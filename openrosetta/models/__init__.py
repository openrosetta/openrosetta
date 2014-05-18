from ming import Session, create_datastore
from ming.odm import Mapper, ThreadLocalODMSession
import os
from pyramid.tweens import EXCVIEW
from webob import exc

session = Session()
DBSession = ThreadLocalODMSession(session)


def ming_autoflush_tween(handler, registry):
    flush_on_errors = (exc.HTTPRedirection,)

    def _cleanup_request():
        ThreadLocalODMSession.flush_all()
        ThreadLocalODMSession.close_all()

    def autoflush(request):
        try:
            response = handler(request)
            _cleanup_request()
            return response
        except flush_on_errors, exc:
            _cleanup_request()
            raise
        except:
            ThreadLocalODMSession.close_all()
            raise

    return autoflush


def includeme(config):
    engine = create_datastore(os.getenv(config.registry.settings['mongo_url_env'], 'openrosetta'))
    session.bind = engine
    Mapper.compile_all()

    for mapper in Mapper.all_mappers():
        session.ensure_indexes(mapper.collection)

    config.add_tween('openrosetta.models.ming_autoflush_tween', over=EXCVIEW)

from babylon import Dataset, HomerQ
