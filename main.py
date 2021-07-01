from flask import Flask, request

from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # creating a new Flask app
api = Api(app)  # wrap our app in a rest API
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # nullable=not_required
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "Video(name={}, views={}, likes={}".format(
            self.name, self.views, self.likes
        )


# db.create_all()  # only do this once

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

video_update_args = reqparse.RequestParser()
video_update_args.add_argument(
    "name", type=str, help="name of the video required",
)
video_update_args.add_argument(
    "views", type=int, help="views on the video required",
)
video_update_args.add_argument(
    "likes", type=int, help="likes on the video required",
)

# videos = {}


# def abort_missing_vid(video_id):
#     if video_id not in videos:
#         abort(404, message="Video id is not valid...")  # abort requires status code


# def abort_vid_exists(video_id):
#     if video_id in videos:
#         abort(409, "Video already exists with that ID")


resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer,
}


class Video(Resource):
    @marshal_with(
        resource_fields
    )  # serialized return value using resource fields (returns dictionary)
    def get(self, video_id):
        # abort_missing_vid(video_id)
        # return videos[video_id]
        # return videos

        result = VideoModel.query.filter_by(id=video_id).first()
        # returns video model object
        if not result:
            abort(404, message=f"could not find video with id: {video_id}")
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        # request.method will tell us that this is a put
        # print(request.form["likes"])
        # abort_vid_exists(video_id)
        args = video_put_args.parse_args()
        # videos[video_id] = args
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="video id taken...")

        video = VideoModel(
            id=video_id, name=args["name"], views=args["views"], likes=args["likes"]
        )
        db.session.add(video)  # temporarily adding video to db
        db.session.commit()  # permanently adding video to db
        return video, 201  # we can return a status code alongside

    @marshal_with(resource_fields)
    def patch(self, video_id):
        # only sending partial information to be updated
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message=f"video: {video_id} does not exist")

        if args['name']:
            result.name = args['name']
        if args["views"]:
            result.views = args['views']
        if args["likes"]:
            result.likes = args['likes']

        db.session.commit() # it's already in the db just need to update it

        return result

    def delete(self, video_id):
        abort_missing_vid(video_id)
        del videos[video_id]
        return "", 204


api.add_resource(
    Video, "/video/<int:video_id>"
)  # adding a resource is like adding an endpoint

if __name__ == "__main__":
    app.run(debug=True)