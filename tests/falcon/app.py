
import falcon
from falcon_redis_cache.middleware import RedisCacheMiddleware
from tests.falcon.resource import TestResource, TestUniqueResource, TestCollectionResource

api = falcon.API(middleware=[PaginationProcessor(), UserProcessor(), CacheProvider(), MultipartMiddleware()])

api.add_error_handler(Exception, ErrorHandler.unexpected)
api.add_error_handler(falcon.HTTPError, ErrorHandler.http)
api.add_error_handler(falcon.HTTPStatus, ErrorHandler.http)

api.add_route(BlogSettingsResource.route, BlogSettingsResource())
api.add_route(CommentResource.route, CommentResource())
api.add_route(PostResource.route, PostResource())
api.add_route(PostCollectionResource.route, PostCollectionResource())
api.add_route(PostSearchResource.route, PostSearchResource())
api.add_route(PostCommentResource.route, PostCommentResource())
api.add_route(PostLikeResource.route, PostLikeResource())
api.add_route(PostViewResource.route, PostViewResource())
api.add_route(UserAuthenticationResource.route, UserAuthenticationResource())
api.add_route(UserRegistrationResource.route, UserRegistrationResource())
api.add_route(UserResource.route, UserResource())
api.add_route(UserAvatarMediaResource.route, UserAvatarMediaResource())
api.add_route(UserAvatarResource.route, UserAvatarResource())
api.add_route(ServiceDescriptionResource.route, ServiceDescriptionResource())

