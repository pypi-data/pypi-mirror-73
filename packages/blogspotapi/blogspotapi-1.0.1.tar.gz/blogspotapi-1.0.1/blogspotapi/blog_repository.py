from pymongo import MongoClient
from .blog_client import BlogPost
from amaraapi import AmaraTools, AmaraVideo
import traceback
import sys
from datetime import datetime, timedelta
import logging

class BlogRepository:
    older_date = datetime.utcnow() + timedelta(-30)
    updated_month_ago = {"last_updated": {"$lte": older_date}}
    never_updated = {"last_updated": {"$exists": False}}
    invalid = {"valid": False}

    def __init__(self, mongo_connection, blogId):
        self.mongo_connect = mongo_connection
        self.client = MongoClient(mongo_connection)
        self.musicblogs_database = self.client.musicblogs
        self.blogId = blogId
        self.posts_collection = self.musicblogs_database['posts.' + blogId]
        self.subtitles_collection = self.musicblogs_database['subtitles.' + blogId]

    def iterate_posts(self):
        return self.posts_collection.find()

    def get_subtitles_for(self, video_url):
        sub_titles_rec = self.subtitles_collection.find_one({"video_url": video_url})
        if sub_titles_rec:
            return sub_titles_rec['subtitles']

    def update_blog_post(self, blog_post):
        if not blog_post:
            return

        if not hasattr(blog_post, "postId"):
            return

        update_key, update_value = {'postId': blog_post.postId}, {k: v for k, v in blog_post._asdict().items()}
        result = self.posts_collection.replace_one(
            filter=update_key,
            replacement=update_value,
            upsert=True)


        logging.debug(f'Updated {blog_post.postId} : {result.matched_count}, {result.modified_count}, {result.upserted_id}')

    def update_sub_titles(self, blog_post, languages, amara_headers):

        amara_tools = AmaraTools(amara_headers)
        if hasattr(blog_post, "labels"):
            labels = blog_post.labels
            video_url = blog_post.videoId

            if labels and ('subtitled' in labels or 'SUBTITLED' in labels):
                found = False
                logging.debug("Trying to get video for {}".format(video_url))
                try:
                    amara_id = amara_tools.get_video_id(video_url='https://youtu.be/' + video_url)
                    amara_video = AmaraVideo(amara_headers, amara_id)
                    if amara_video:
                        logging.debug(f'Found video in Amara: {amara_id}')
                        languages_video = amara_video.get_languages()
                        common_languages = [l['code'] for l in languages_video if l['code'] in languages]
                        if common_languages:
                            logging.debug("Found languages : {}".format(common_languages))
                            all_subtitles = [amara_video.get_subtitles(sel_language) for sel_language in common_languages]
                            valid_subtitles = [subtitle for subtitle in all_subtitles if subtitle and len(subtitle['subtitles']) > 0 and '-->' in subtitle['subtitles']]
                            if valid_subtitles:
                                subtitles = valid_subtitles[0]
                                version_number = subtitles.get('version_number', 1)
                                lang = subtitles['language']["code"]
                                logging.debug("Saving subtitles for {}, v{}, {}".format(video_url, version_number, lang))
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

    def delete_old_posts(self):
        self.posts_collection.remove(self.updated_month_ago)
        self.posts_collection.remove(self.never_updated)
        self.posts_collection.remove(self.invalid)

    def delete_old_subtitles(self):
        self.subtitles_collection.remove(self.updated_month_ago)
        self.subtitles_collection.remove(self.never_updated)
        self.subtitles_collection.remove(self.invalid)

    def invalidate_link(self, post_id, video_url):
        logging.info("Invalidating POST {post_id} containing video {video_url}")
        self.posts_collection.update({'postId': post_id}, {'$set': self.invalid})
        self.subtitles_collection.update({'video_url': video_url}, {'$set': self.invalid})