from flask import Flask, request

from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)  # creating a new Flask app
api = Api(app)  # wrap our app in a rest API

"""
names = {"tim": {"age": 19, "gender": "male"}, "japjot": {"age": 21, "gender": "male"}}
# creating a resource
class HelloWorld(Resource):
    def get(self, name):
        # return {
        #     "data": "Hello World, {}".format(name)
        # }  # dictionary b/c that is JSON serializable

        return names[name]

    def post(self):
        return {"data": "posted"}    
# how to find the HelloWorld resource
api.add_resource(HelloWorld, "/helloworld/<string:name>")
"""

video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "name", type=str, help="name of the video required", required=True
)
video_put_args.add_argument(
    "views", type=int, help="views on the video required", required=True
)
video_put_args.add_argument(
    "likes", type=int, help="likes on the video required", required=True
)

videos = {}


def abort_missing_vid(video_id):
    if video_id not in videos:
        abort(404, message="Video id is not valid...")  # abort requires status code


def abort_vid_exists(video_id):
    if video_id in videos:
        abort(409, "Video already exists with that ID")


class Video(Resource):
    def get(self, video_id):
        abort_missing_vid(video_id)
        return videos[video_id]

        # return videos

    def put(self, video_id):
        # request.method will tell us that this is a put
        # print(request.form["likes"])
        abort_vid_exists(video_id)
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201  # we can return a status code alongside

    def delete(self, video_id):
        abort_missing_vid(video_id)
        del videos[video_id]
        return "", 204


api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)