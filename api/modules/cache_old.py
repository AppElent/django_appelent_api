#from .encryption import encrypt_message, decrypt_message, generate_key
#key = generate_key()
from django.core.cache import cache as djangocache
from django_redis import get_redis_connection
con = get_redis_connection("default")

djangocache.get_keys = "hallo"

class Cache():

    _cache = {
        'global': {}
    }

    def get_cachekey(self, **kwargs):
        key = kwargs.get('key')
        userid = kwargs.get('userid')
        category = kwargs.get('category')

        if not userid and key:
            cachekey = key
        elif userid and not key and not category:
            cachekey = str(userid)
        elif userid and category and not key:
            cachekey = str(userid) + '.' + category
        elif userid and category and key:
            cachekey = str(userid) + '.' + category + '.' + key
        else:
            print('Key niet gevonden (key, userid, category)', key, userid, category)
        return cachekey
    
    delimiter = '~~~'

    def get_keys(self, **kwargs):
        allkeys = djangocache.get('allkeys', default='')
        return allkeys.split(self.delimiter)

    def add_key(self, key, **kwargs):
        allkeys = djangocache.get('allkeys', default='')
        allkeys = allkeys.split(self.delimiter)
        if key not in allkeys:
            allkeys.append(key)
            allkeys = self.delimiter.join(allkeys)
            djangocache.set('allkeys', allkeys)

    def delete_key(self, key, **kwargs):
        allkeys = djangocache.get('allkeys', default='')
        allkeys = allkeys.split(self.delimiter)

        try:
            allkeys.remove(key)
            allkeys = self.delimiter.join(allkeys)
            djangocache.set('allkeys', allkeys)
        except:
            pass
    
    def delete_keys(self, keys, **kwargs):
        allkeys = djangocache.get('allkeys', default='')
        allkeys = allkeys.split(self.delimiter)

        for key in keys:
            try:
                allkeys.remove(key)
            except:
                pass
        allkeys = self.delimiter.join(allkeys)
        djangocache.set('allkeys', allkeys)


    def get(self, key, **kwargs):
        kwargs['key'] = key
        if key == "all":
            return djangocache.get('*')
        cachekey = self.get_cachekey(**kwargs)
        return djangocache.get(cachekey)

    def set(self, key, value, timeout=None, **kwargs):
        kwargs['key'] = key
        cachekey = self.get_cachekey(**kwargs)
        self.add_key(cachekey)
        djangocache.set(cachekey, value, timeout)

    def delete(self, key, **kwargs):
        kwargs['key'] = key
        cachekey = self.get_cachekey(**kwargs)
        self.delete_key(cachekey)
        djangocache.delete(cachekey)
    


cache = Cache()

if __name__ == "__main__":
    user1 = {'id': 100}
    user2 = {'id': 101}
    user3 = {'id': 102}
    cache.set(userid=user1['id'], category='solaredge', key='token', value='<tokenhere>1')
    cache.set(userid=user2['id'], category='solaredge', key='token', value='<tokenhere>2')
    cache.set(userid=user3['id'], category='solaredge', key='token', value='<tokenhere>3')
    cache.set(userid=user1['id'], category='solaredge', key='setting1', value='<tokenhere>1')
    cache.set(userid=user1['id'], category='solaredge', key='setting2', value='<tokenhere>2')
    cache.set(userid=user1['id'], category='solaredge', key='setting3', value='<tokenhere>3')
    cache.set(userid=user1['id'], category='solaredge', key='setting4', value='<tokenhere>4')

    
    cache.delete(userid=user3['id'], category='solaredge')
    cache.delete(userid=user1['id'], category='solaredge', key='setting2')

    cache.delete(userid=user2['id'])

    print('Get1', cache.get(userid=100))
    print('Get2', cache.get(userid=102, category='solaredge'))
    print('Get3', cache.get(userid=100, category='solaredge', key='setting3'))
    print('Get4', cache.get(userid=100, category='solaredge', key='setting4'))
