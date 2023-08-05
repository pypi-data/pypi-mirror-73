import requests
import json
import base64
import random
from Sakurajima.models import (
    Anime,
    RecommendationEntry,
    Relation,
    AniWatchEpisode,
    Episode,
    ChronicleEntry,
    UserAnimeListEntry,
    UserMedia,
    UserOverview,
    AniwatchStats,
    Notification,
    WatchListEntry,
    Media,
)
from Sakurajima.utils.episode_list import EpisodeList


class Sakurajima:
    def __init__(
        self,
        username=None,
        userId=None,
        authToken=None,
        endpoint="https://aniwatch.me/api/ajax/APIHandle",
    ):
        xsrf_token = self.__generate_xsrf_token()
        self.userId = userId
        self.headers = {
            "x-xsrf-token": xsrf_token,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        }
        self.cookies = {"xsrf-token": xsrf_token}

        self.API_URL = endpoint
        if username is not None and userId is not None and authToken is not None:
            self.headers["x-auth"] = authToken
            session_token = (
                '{"userid":'
                + str(userId)
                + ',"username":"'
                + str(username)
                + '","usergroup":4,"player_lang":1,"player_quality":0,"player_time_left_side":2,"player_time_right_side":3,"screen_orientation":1,"nsfw":1,"chrLogging":1,"mask_episode_info":0,"blur_thumbnails":0,"autoplay":1,"preview_thumbnails":1,"update_watchlist":1,"playheads":1,"seek_time":5,"cover":null,"title":"Member","premium":1,"lang":"en-US","auth":"'
                + str(authToken)
                + '","remember_login":true}'
            )
            self.cookies["SESSION"] = session_token
            self.headers[
                "COOKIE"
            ] = f"SESSION={session_token}; XSRF-TOKEN={xsrf_token};"

    def __generate_xsrf_token(self):
        characters = [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
        ]
        return "".join(random.choice(characters) for i in range(32))

    def __post(self, data):
        with requests.post(
            self.API_URL, headers=self.headers, json=data, cookies=self.cookies
        ) as url:
            return json.loads(url.text)

    def get_episode(self, episode_id, lang="en-US"):
        data = {
            "controller": "Anime",
            "action": "watchAnime",
            "lang": lang,
            "ep_id": episode_id,
            "hoster": "",
        }
        return AniWatchEpisode(self.__post(data), episode_id)

    def get_episodes(self, anime_id):
        data = {
            "controller": "Anime",
            "action": "getEpisodes",
            "detail_id": str(anime_id),
        }
        return EpisodeList(
            [
                Episode(data_dict, self.headers, self.cookies, self.API_URL, anime_id)
                for data_dict in self.__post(data)["episodes"]
            ]
        )

    def get_anime(self, anime_id):
        data = {"controller": "Anime", "action": "getAnime", "detail_id": str(anime_id)}
        return Anime(
            self.__post(data)["anime"],
            headers=self.headers,
            cookies=self.cookies,
            api_url=self.API_URL,
        )

    def get_recommendations(self, anime_id):
        data = {
            "controller": "Anime",
            "action": "getRecommendations",
            "detail_id": str(anime_id),
        }
        return [
            RecommendationEntry(data_dict, self.headers, self.cookies, self.API_URL)
            for data_dict in self.__post(data)["entries"]
        ]

    def get_relation(self, relation_id):
        data = {
            "controller": "Relation",
            "action": "getRelation",
            "relation_id": relation_id,
        }
        return Relation(self.__post(data)["relation"])

    def get_seasonal_anime(self, index="null", year="null"):
        data = {
            "controller": "Anime",
            "action": "getSeasonalAnime",
            "current_index": index,
            "current_year": year,
        }
        return [
            Anime(data_dict, self.headers, self.cookies, self.API_URL)
            for data_dict in self.__post(data)["entries"]
        ]

    def get_latest_releases(self):
        data = {"controller": "Anime", "action": "getLatestReleases"}
        return [
            Anime(data_dict, self.headers, self.cookies, self.API_URL)
            for data_dict in self.__post(data)["entries"]
        ]

    def get_latest_uploads(self):
        data = {"controller": "Anime", "action": "getLatestUploads"}
        return [
            Anime(data_dict, self.headers, self.cookies, self.API_URL)
            for data_dict in self.__post(data)["entries"]
        ]

    def get_latest_anime(self):
        data = {"controller": "Anime", "action": "getLatestAnime"}
        return [
            Anime(data_dict, self.headers, self.cookies, self.API_URL)
            for data_dict in self.__post(data)["entries"]
        ]

    def get_random_anime(self):
        data = {"controller": "Anime", "action": "getRandomAnime"}
        return Anime(
            self.__post(data)["entries"][0], self.headers, self.cookies, self.API_URL
        )

    def get_airing_anime(self, randomize=False):
        data = {
            "controller": "Anime",
            "action": "getAiringAnime",
            "randomize": randomize,
        }
        airing_anime_response = self.__post(data)["entries"]
        airing_anime = {}
        for day, animes in airing_anime_response.items():
            airing_anime[day] = [
                Anime(anime_dict, self.headers, self.cookies, self.API_URL)
                for anime_dict in animes
            ]
        return airing_anime

    def get_popular_anime(self, page=1):
        data = {"controller": "Anime", "action": "getPopularAnime", "page": page}
        return [
            Anime(data_dict, self.headers, self.cookies, self.API_URL)
            for data_dict in self.__post(data)["entries"]
        ]

    def get_popular_seasonal_anime(self, page=1):
        data = {"controller": "Anime", "action": "getPopularSeasonals", "page": page}
        return [
            Anime(data_dict, self.headers, self.cookies, self.API_URL)
            for data_dict in self.__post(data)["entries"]
        ]

    def get_popular_upcoming_anime(self, page=1):
        data = {"controller": "Anime", "action": "getPopularUpcomings", "page": page}
        return [
            Anime(data_dict, self.headers, self.cookies, self.API_URL)
            for data_dict in self.__post(data)["entries"]
        ]

    def get_hot_anime(self, page=1):
        data = {"controller": "Anime", "action": "getHotAnime", "page": page}
        return [
            Anime(data_dict, self.headers, self.cookies, self.API_URL)
            for data_dict in self.__post(data)["entries"]
        ]

    def get_best_rated_anime(self, page=1):
        data = {"controller": "Anime", "action": "getBestRatedAnime", "page": page}
        return [
            Anime(data_dict, self.headers, self.cookies, self.API_URL)
            for data_dict in self.__post(data)["entries"]
        ]

    def add_recommendation(self, anime_id, recommended_anime_id):
        data = {
            "controller": "Anime",
            "action": "addRecommendation",
            "detail_id": str(anime_id),
            "recommendation": str(recommended_anime_id),
        }
        return self.__post(data)

    def get_stats(self):
        data = {"controller": "XML", "action": "getStatsData"}
        return AniwatchStats(self.__post(data))

    def get_user_overview(self):
        data = {
            "controller": "Profile",
            "action": "getOverview",
            "profile_id": str(self.userId),
        }
        return UserOverview(self.__post(data)["overview"])

    def get_user_chronicle(self, page=1):
        data = {
            "controller": "Profile",
            "action": "getChronicle",
            "profile_id": str(self.userId),
            "page": page,
        }
        return [
            ChronicleEntry(data_dict, self.headers, self.cookies, self.API_URL)
            for data_dict in self.__post(data)["chronicle"]
        ]

    def get_user_anime_list(self):
        data = {
            "controller": "Profile",
            "action": "getAnimelist",
            "profile_id": str(self.userId),
        }
        return [
            UserAnimeListEntry(data_dict, self.headers, self.cookies, self.API_URL)
            for data_dict in self.__post(data)["animelist"]
        ]

    def get_user_media(self, page=1):
        data = {
            "controller": "Profile",
            "action": "getMedia",
            "profile_id": str(self.userId),
            "page": page,
        }
        return [
            UserMedia(data_dict, self.headers, self.cookies, self.API_URL)
            for data_dict in self.__post(data)["entries"]
        ]

    def send_image_to_discord(self, episode_id, base64_image, episode_time):
        data = {
            "controller": "Profile",
            "action": "sendToDiscord",
            "file": base64_image,
            "episode_id": int(episode_id),
            "time": episode_time,
            "lang": "en-US",
        }
        return self.__post(data)

    def get_user_friends(self, page=1):
        data = {"controller": "Profile", "action": "getFriends", "page": page}
        return self.__post(data)

    def add_friend(self, friend_user_id):
        data = {
            "controller": "Profile",
            "action": "addFriend",
            "profile_id": friend_user_id,
        }
        return self.__post(data)

    def remove_friend(self, friend_id):
        data = {
            "controller": "Profile",
            "action": "removeFriend",
            "friend_id": friend_id,
        }
        return self.__post(data)

    def withdraw_friend_request(self, friend_id):
        data = {
            "controller": "Profile",
            "action": "withdrawRequest",
            "friend_id": friend_id,
        }
        return self.__post(data)

    def accept_friend_request(self, friend_id):
        data = {
            "controller": "Profile",
            "action": "acceptRequest",
            "friend_id": friend_id,
        }
        return self.__post(data)

    def reject_friend_request(self, friend_id):
        data = {
            "controller": "Profile",
            "action": "rejectRequest",
            "friend_id": friend_id,
        }
        return self.__post(data)

    def get_user_settings(self):
        data = {"controller": "Profile", "action": "getSettings"}
        return self.__post(data)

    def get_notifications(self):
        data = {"controller": "Profile", "action": "getNotifications"}
        return [
            Notification(data_dict, self.headers, self.cookies, self.API_URL)
            for data_dict in self.__post(data)["notifications"]
        ]

    def mark_all_notifications_as_read(self):
        data = {
            "controller": "Profile",
            "action": "markAllNotificationsAsRead",
            "view": 0,
        }
        return self.__post(data)

    def delete_all_notifications(self):
        data = {"controller": "Profile", "action": "deleteAllNotifications", "view": 0}
        return self.__post(data)

    def toggle_notification_seen(self, notification_id):
        data = {
            "controller": "Profile",
            "action": "toggleNotificationSeen",
            "id": notification_id,
        }
        return self.__post(data)

    def delete_notification(self, notification_id):
        data = {
            "controller": "Profile",
            "action": "deleteNotification",
            "id": notification_id,
        }
        return self.__post(data)

    def get_anime_chronicle(self, anime_id, page=1):
        data = {
            "controller": "Profile",
            "action": "getChronicle",
            "detail_id": str(anime_id),
            "page": page,
        }
        return [
            ChronicleEntry(data_dict, self.headers, self.cookies, self.API_URL)
            for data_dict in self.__post(data)["chronicle"]
        ]

    def remove_chronicle_entry(self, chronicle_id):
        data = {
            "controller": "Profile",
            "action": "removeChronicleEntry",
            "chronicle_id": chronicle_id,
        }
        return self.__post(data)

    def get_discord_hash(self):
        data = {"controller": "Profile", "action": "getDiscordHash"}
        return self.__post(data)

    def renew_discord_hash(self):
        data = {"controller": "Profile", "action": "renewDiscordHash"}
        return self.__post(data)

    def remove_discord_verification(self):
        data = {"controller": "Profile", "action": "removeDiscordVerification"}
        return self.__post(data)

    def get_unread_notifications(self):
        data = {"controller": "Profile", "action": "getUnreadNotifications"}
        return [
            Notification(data_dict, self.headers, self.cookies, self.API_URL)
            for data_dict in self.__post(data)["notifications"]
        ]

    def toggle_mark_as_watched(self, anime_id, episode_id):
        data = {
            "controller": "Profile",
            "action": "markAsWatched",
            "detail_id": str(anime_id),
            "episode_id": episode_id,
        }
        return self.__post(data)

    def mark_as_completed(self, anime_id):
        data = {
            "controller": "Profile",
            "action": "markAsCompleted",
            "detail_id": str(anime_id),
        }
        return self.__post(data)

    def mark_as_plan_to_watch(self, anime_id):
        data = {
            "controller": "Profile",
            "action": "markAsPlannedToWatch",
            "detail_id": str(anime_id),
        }
        return self.__post(data)

    def mark_as_on_hold(self, anime_id):
        data = {
            "controller": "Profile",
            "action": "markAsOnHold",
            "detail_id": str(anime_id),
        }
        return self.__post(data)

    def mark_as_dropped(self, anime_id):
        data = {
            "controller": "Profile",
            "action": "markAsDropped",
            "detail_id": str(anime_id),
        }
        return self.__post(data)

    def mark_as_watching(self, anime_id):
        data = {
            "controller": "Profile",
            "action": "markAsWatching",
            "detail_id": str(anime_id),
        }
        return self.__post(data)

    def remove_from_list(self, anime_id):
        data = {
            "controller": "Profile",
            "action": "removeAnime",
            "detail_id": str(anime_id),
        }
        return self.__post(data)

    def favorite_media(self, media_id):
        data = {"controller": "Media", "action": "favMedia", "media_id": str(media_id)}
        return self.__post(data)

    def rateAnime(self, anime_id, rating):
        # Rate 0 to remove rating
        data = {
            "controller": "Profile",
            "action": "rateAnime",
            "detail_id": str(anime_id),
            "rating": rating,
        }
        return self.__post(data)

    def get_reports(self):
        data = {"controller": "Profile", "action": "getReports"}
        return self.__post(data)

    def report_missing_anime(self, anime_name):
        data = {
            "controller": "Anime",
            "action": "reportMissingAnime",
            "anime_name": str(anime_name),
        }
        return self.__post(data)

    def report_missing_streams(self, anime_id):
        data = {
            "controller": "Anime",
            "action": "reportMissingStreams",
            "detail_id": str(anime_id),
        }
        return self.__post(data)

    def get_watchlist(self, page=1):
        data = {
            "controller": "Anime",
            "action": "getWatchlist",
            "detail_id": 0,
            "page": page,
        }
        return [
            WatchListEntry(data_dict, self.headers, self.cookies, self.API_URL)
            for data_dict in self.__post(data)["entries"]
        ]

    def login(self, username, password):
        data = {
            "username": username,
            "password": base64.b64encode(bytes(password, "utf8")).decode("utf8"),
            "code": "",
            "controller": "Authentication",
            "action": "doLogin",
        }
        return self.__post(data)

    def forgot_password(self, email):
        data = {
            "controller": "Authentication",
            "action": "doForgotPW",
            "email": base64.b64encode(bytes(email, "utf8")).decode("utf8"),
        }
        return self.__post(data)

    def search(self, query):
        data = {
            "controller": "Search",
            "action": "search",
            "rOrder": False,
            "order": "title",
            "typed": str(query),
            "genre": "[]",
            "staff": "[]",
            "tags": [],
            "langs": [],
            "anyGenre": False,
            "anyStaff": False,
            "anyTag": False,
            "animelist": [2],
            "types": [0],
            "status": [0],
            "yearRange": [1965, 2022],
            "maxEpisodes": 0,
            "hasRelation": False,
        }
        return [
            Anime(data_dict, self.headers, self.cookies, self.API_URL)
            for data_dict in self.__post(data)
        ]

    def get_media(self, anime_id):
        data = {"controller": "Media", "action": "getMedia", "detail_id": str(anime_id)}
        return Media(
            self.__post(data), self.headers, self.cookies, self.API_URL, anime_id
        )
