from pymongo import MongoClient
from .blog_client import BlogPost
from amaraapi import AmaraTools, AmaraVideo
import traceback
import sys
from datetime import date, datetime, timedelta

class BlogRepository:

    def __init__(self, mongo_connection, blogId):
        self.mongo_connect = mongo_connection
        self.client = MongoClient(mongo_connection)
        self.musicblogs_database = self.client.musicblogs
        self.blogId = blogId
        self.posts_collection = self.musicblogs_database['posts.' + blogId]
        self.posts_in_blog = self.posts_collection.find()
        self.posts_map = \
            {p['postId']: BlogPost(
                postId=p['postId'], title=p['title'], videoId=p['videoId'], content=p['content'],
                labels=p.get('labels', 0),
                url=p.get('url', ''),
                amara_embed=p.get('amara_embed', ''), last_updated=datetime.utcnow()
            ) for p in self.posts_in_blog
            }

        self.postids = set(self.posts_map.keys())
        self.subtitles_collection = self.musicblogs_database['subtitles.' + blogId]


    def get_subtitles_for(self, video_url):
        sub_titles_rec = self.subtitles_collection.find_one({"video_url": video_url})
        if sub_titles_rec:
            return sub_titles_rec['subtitles']

    def update_blog_post(self, blog_post):
        if not blog_post:
            return

        if not hasattr(blog_post, "postId"):
            return
        if blog_post.postId in self.postids:
            self.postids.remove(blog_post.postId)

        if blog_post.postId in self.posts_map:

            update_key, update_value = {'postId': blog_post.postId}, {k: v for k, v in blog_post._asdict().items() if k not in "postId"}

            if blog_post != self.posts_map[blog_post.postId]:
                print("updating {}".format(update_key ))

                self.posts_collection.update_one(update_key,   { '$set' : update_value } )
                print("updated {} ".format(update_key))
            else:
                print("post {} unchanged".format(blog_post.postId))
        else:
            print("inserting {} ".format(blog_post.postId))
            self.posts_collection.insert_one(blog_post._asdict())
            print("inserted {} ".format(blog_post.postId))

    def update_sub_titles(self, blog_post, languages, amara_headers):

        amara_tools = AmaraTools(amara_headers)
        if hasattr(blog_post, "labels"):
            labels = blog_post.labels
            video_url = blog_post.videoId

            if labels and ('subtitled' in labels or 'SUBTITLED' in labels):
                found = False
                print("Trying to get video for {}".format(video_url))
                try:
                    amara_id = amara_tools.get_video_id(video_url='https://youtu.be/' + video_url)
                    amara_video = AmaraVideo(amara_headers, amara_id)
                    if amara_video:
                        print("Found video in Amara")
                        languages_video = amara_video.get_languages()
                        common_languages = [l['code'] for l in languages_video if l['code'] in languages]
                        if common_languages:
                            print("Found languages : {}".format(common_languages))
                            all_subtitles = [amara_video.get_subtitles(sel_language) for sel_language in common_languages]
                            valid_subtitles = [subtitle for subtitle in all_subtitles if subtitle and len(subtitle['subtitles']) > 0 and '-->' in subtitle['subtitles']]
                            if valid_subtitles:
                                subtitles = valid_subtitles[0]
                                version_number = subtitles.get('version_number', 1)
                                lang = subtitles['language']["code"]
                                print("Saving subtitles for {}, v{}, {}".format(video_url, version_number, lang))
                                self.subtitles_collection.replace_one(
                                    filter={"video_url": video_url, "version_number": version_number},
                                    replacement={"video_url": video_url, "video_id": amara_id,
                                                 "lang": subtitles['language'],
                                                 "subtitles": subtitles['subtitles'],
                                                 "version_number": version_number,
                                                 "last_updated": datetime.utcnow()},
                                    upsert=True,

                                )
                                found = True

                except:
                    traceback.print_exc(file=sys.stderr)
                    print("Could not process {} from {}".format(video_url, blog_post.url))
                if not found:
                    print("Could not find subtitles for {}, {}".format(video_url, blog_post.url))
        self.subtitles_collection.remove(
                {"version_number": {"$exists": False}},
        )

    def delete_invalid_posts(self):
        for postid in self.postids:
            self.posts_collection.delete_one({'postId': postid})
            print("post {} deleted".format(postid))

    def delete_old_posts(self):

        older_date = datetime.utcnow() + timedelta(-30)
        remove_criteria = {"last_updated":{"$lte": older_date}}

        self.posts_collection.remove(remove_criteria)
        self.subtitles_collection.remove(remove_criteria)


    def save_to_videos(self):
        videos_collection = self.musicblogs_database['blog_videos.' + str(self.blogId)]

        for postId, blog_post in self.posts_map.items():
            videoId = blog_post.videoId
            replacement = {"videoId": videoId, "title": blog_post.title, "blogId": self.blogId, "postId": postId,
                           "last_updated": datetime.utcnow()}

            videos_collection.replace_one(
                filter={"blogId": self.blogId, "postId": postId},
                replacement=replacement,
                upsert=True
            )