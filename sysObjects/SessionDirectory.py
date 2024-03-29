"""
Container for Sessions that may communicate with eachother.

Sessions within the same SessionDirectory may communicate and interact with eachother, allowing for objects across
sessions to interact.
"""

# TODO: Posts should be their own objects. Please...
from threading import Thread
from sysObjects.Tagable import Tagable


class SessionDirectory(Thread, Tagable):
    """
    A container for Sessions that allows for interactions across sessions.

    **Attributes**:
        * **pendForAll** `bool`: Toggle for pending all sessions or just the necessary ones.
        * **removeDeadSessions** `bool`: Toggle for removing sessions from sessionList if they are dead.
        * **killOnSessionsDead** `bool`: Toggle to kill the directory if there are no alive Sessions in sessionList.
        * **sessionList** `list`: List of all (:py:class:`sysObjects.Session.Session`) that can interact with eachother.
        * **posts** `list`: List of all requests made by sessions to the directory.
        * **live** `bool`: Weather or not the directory thread should die.
        * **tags** `dict`: Tags

    **Tags**:
        * **id** `str`: The id.
        * **errs** `list`: List of exceptions raised in the directory.
            Does not contain exceptions raised by sessions.
        * **postLog** `list`: Log of posts executed.
            Log format: (function, source id)
        * **permissions** `[whitelist, blacklist]`: List of permissions.

    :param str dirId: The id of this directory.
    :param ses: List of sessions to start with, defaults to an empty list.
    :type ses: list, optional
    :param tags: Tags. The ``id`` tag will be set to ``dirId``.
    :type tags: dict, optional
    """

    def __init__(self, dirId, ses=None, tags=None):
        """
        Constructor
        """
        super().__init__()
        if tags is None:
            self.tags = {}
        else:
            self.tags = tags
        if ses is None:
            self.sessionList = []
        else:
            self.sessionList = ses
        self.pendForAll = False
        self.removeDeadSessions = False
        self.killOnSessionsDead = True
        self.posts = []
        self.live = True
        self.tags["id"] = dirId
        self.tags["permissions"] = [
            [  # allowed
                ("all", "crossWarp")
            ],
            [  # blocked
                ("all", "all")
            ]
        ]
        self.tags["errs"] = []
        self.tags["postLog"] = []

    def __str__(self):
        aliveOrNot = "Dead"
        if self.live:
            aliveOrNot = "Alive"
        return "{}:{}:sessions {}".format(self.tags["id"], aliveOrNot, self.sessionList.__len__())

    def takePost(self, post):
        """
        Take post and add it to posts.

        A post is a `list` with three elements.
          * `str` **Function**: The function to call as a string. Must be a member of this class, extend it to add more methods.
          * `list` **Paramaters**: List of parameters to pass to the function.
          * `str` **Source**: Id of object that made the request.

        A Session calls this in its execute().

        :param list post: The post to take.
        """
        # post format:[funct, [prams], source]
        self.posts.append(post)

    def handlePost(self, post):
        """
        Handle a post and remove it from the posts list.

        :param list post: Post to handle.
        """
        self.resolve(post)
        self.execute(post)
        self.log(post)
        self.posts.remove(post)

    def resolve(self, post):
        """
        Replace params in post with intended values.

        Will replace a string `"src"` with the source object and valid session ids to references to those sessions.

        :param list post: Post to resolve parameters of.
        """
        pramLen = post[1].__len__()
        pramRange = range(pramLen)
        for pIdx in pramRange:
            pram = post[1][pIdx]
            if pram == "src":  # Replacement for source
                post[1][pIdx] = post[2]

            elif isinstance(pram, str):  # Replace sesId with ses.
                for ses in self.sessionList:
                    if pram == ses.tags["id"]:
                        post[1][pIdx] = ses
                        break

    def execute(self, post):
        """
        Call a method dependent on post.

        Exceptions will be logged to this object's "errs" tag.

        :param list post: Info for what method to call and with what parameters
        """
        try:
            if post[1]:
                getattr(self, post[0])(*post[1])
            else:
                getattr(self, post[0])()
        except BaseException as e:
            if not isinstance(e, StopIteration):
                self.tags["errs"].append(e)  # Log error

    def log(self, post):
        """
        Log post to postLog tag.

        :param list post: Post to log.
        """
        # Format: (function, source id)
        if isinstance(post[2], str):
            p2 = post[2]
        else:
            p2 = post[2].tags["id"]
        self.tags["postLog"].append((post[0], p2))

    def pendSessions(self, sessions):
        """
        Pend all the sessions in list sessions.

        if self.pendForAll is True then pend all sessions in this directory.

        :param list sessions: The list of sessions to pend.
        """
        if self.pendForAll:  # If enabled: pend ALL sessions.
            sessions = self.sessionList
        for ses in sessions:  # Send pend request.
            ses.pendRequest = True
        while True:
            count = 0
            for ses in sessions:
                if ses.pended:
                    count += 1
            if count == sessions.__len__():  # Break when all sessions are pended.
                break

    def unpendSessions(self, sessions):
        """
        Unpend all the sessions in list sessions.

        If self.pendForAll is True then unpend all sessions in this directory.

        :param list sessions: List of sessions to unpend.
        """
        if self.pendForAll:  # If enabled: unpend ALL sessions.
            sessions = self.sessionList
        for ses in sessions:  # Tell sessions to unpend.
            ses.pendRequest = False

    def crossWarp(self, obj, fromSession, toSession, newPos=None):
        """
        Move obj from fromSession to toSession possibly with position of newPos. This is mostly a test method.

        Sessions are pended before action is taken and un-pended afterwards.
        If newPos is None, object's position is unchanged.

        :param object/StaticObject obj: The object to move, must be a StaticObject to set position.
        :param Session fromSession: Session that obj is coming from/ currently in.
        :param Session toSession: Session to put obj in.
        :param Vector3/None newPos: The new position of obj in toSession.
        """
        try:  # Handle bad params from post.
            sesLst = [fromSession, toSession]
            self.pendSessions(sesLst)  # Pend before operation.
            fromSession.objectList.remove(obj)  # Remove obj from fromSession.
            if newPos is not None:  # Set position if possible.
                try:
                    obj.model.position = newPos
                except AttributeError as e:
                    self.tags["errs"].append(e)
            toSession.objectList.append(obj)  # Put obj in toSession.
            self.unpendSessions(sesLst)  # Unpend after operation.
        except BaseException as e:
            if not isinstance(e, StopIteration):
                self.tags["errs"].append(e)  # Log error

    def run(self):
        """
        Obligatory thread run.

        Call with `this.start()`.
        Starts all sessions in sessionList when called.
        """
        for ses in self.sessionList:  # Start all sessions
            ses.directory = self
            ses.start()

        while self.live:
            if self.killOnSessionsDead:  # Handle killOnSessionsDead
                kill = True
                for ses in self.sessionList:
                    if self.removeDeadSessions and not ses.live:  # Handle removeDeadSessions
                        self.sessionList.remove(ses)
                    if ses.live:
                        kill = False
                if kill:
                    self.live = False

            for p in self.posts:  # Handle posts.
                self.handlePost(p)

        for ses in self.sessionList:  # Kill sessions on directory kill.
            ses.live = False
