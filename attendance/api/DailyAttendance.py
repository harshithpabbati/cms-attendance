import graphene
from graphql_jwt.decorators import login_required
from django.utils import timezone
import json

from ..models import Log
from members.models import Group
from django.contrib.auth.models import User
from .User import AttendanceUserBasicObj

to_tz = timezone.get_default_timezone()


class MemberPresentObj(graphene.ObjectType):
    member = graphene.Field(AttendanceUserBasicObj)
    firstSeen = graphene.String()
    lastSeen = graphene.String()
    duration = graphene.String()

    def resolve_member(self, info):
        return User.objects.values().get(id=self['member_id'])

    def resolve_firstSeen(self, info):
        sessions = json.loads(self['sessions'])
        return sessions[0]['start']

    def resolve_lastSeen(self, info):
        return self['lastSeen'].astimezone(to_tz)


class MembersAbsentObj(graphene.ObjectType):
    member = graphene.Field(AttendanceUserBasicObj)
    lastSeen = graphene.String()

    def resolve_member(self, info):
        return User.objects.values().get(username=self)

    def resolve_lastSeen(self, intro):
        obj = Log.objects.filter(member__username=self).order_by('-date').first()
        if obj is not None:
            return obj.lastSeen
        else:
            return None


class DailyAttObj(graphene.ObjectType):
    date = graphene.types.datetime.Date()
    membersPresent = graphene.List(MemberPresentObj)
    membersAbsent = graphene.List(MembersAbsentObj)

    def resolve_date(self, info):
        return self

    def resolve_membersPresent(self, info):
        return Log.objects.values().filter(date=self)

    def resolve_membersAbsent(self, info):
        groups = Group.objects.filter(attendanceEnabled=True).values('members__username')
        logs = Log.objects.values('member__username').filter(date=self)
        LogUsernames = []
        for i in logs:
            LogUsernames.append(i['member__username'])
        usernames = []
        for member in groups:
            username = member['members__username']
            if username not in LogUsernames:
                usernames.append(username)
        return usernames


class Query(object):
    dailyAttendance = graphene.Field(
        DailyAttObj,
        date=graphene.types.datetime.Date(required=True)
    )

    @login_required
    def resolve_dailyAttendance(self, info, **kwargs):
        return kwargs.get('date')
