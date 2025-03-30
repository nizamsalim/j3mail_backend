from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from .models import EncryptedMail
from utils.db import MongoDB
from bson import ObjectId
import datetime

# Create your views here.
mails = MongoDB().db("emails")

ise = Response({"success": False, "error": "Something went wrong", "field": "server"})


class Mail(APIView):
    def post(self, req):
        try:
            mail = EncryptedMail(**(req.data))
            mail.mail["from"] = req.user.email
            now = datetime.datetime.now()
            mail.__dict__["meta"] = {
                "date": now.strftime("%d %b"),
                "time": now.strftime("%I:%M %p"),
                "isUnread": True,
            }
            # print(mail.__dict__)
            res = mails.insert_one(mail.__dict__)
            return Response({"success": True})
        except Exception as e:
            print(e)
            return ise


class ReadMail(APIView):
    def get(self, req: Request):
        try:
            id = req.query_params["id"]
            mail = mails.find_one({"_id": ObjectId(id)})
            r = mails.update_one(
                {"_id": ObjectId(id)}, {"$set": {"meta.isUnread": False}}
            )
            mail["_id"] = str(mail["_id"])
            return Response({"success": True, "mail": mail})
        except Exception as e:
            print(e)
            return ise


class MailList(APIView):
    def get(self, req: Request):
        try:
            list = req.query_params["list"]
            res = []
            if list == "inbox":
                res = mails.find(
                    {"mail.to": req.user.email}, {"mail.from": 1, "meta": 1}
                )

            elif list == "outbox":
                res = mails.find(
                    {"mail.from": req.user.email}, {"mail.to": 1, "meta": 1}
                )
            else:
                return Response(status=400)
            res = res.to_list()
            res.reverse()
            res = [{**r, "_id": str(r["_id"])} for r in res]
            return Response({"success": True, "mails": res})
        except Exception as e:
            print(str(e))
            return ise
