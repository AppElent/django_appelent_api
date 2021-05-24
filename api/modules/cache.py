#from .encryption import encrypt_message, decrypt_message, generate_key
#key = generate_key()

class Cache():

    _cache = {
        'global': {}
    }

    #kwargs userid en category
    def get(self, **kwargs):
        key = kwargs.get('key')
        userid = kwargs.get('userid')
        category = kwargs.get('category')

        if not userid and key:
            return self._cache['global'][key]
        elif userid and not key and not category:
            return self._cache.get(userid)
        elif userid and category and not key:
            try:
                return self._cache[userid][category]
            except:
                return None
        elif userid and category and key:
            try:
                return self._cache[userid][category][key]
            except:
                return None
        else:
            print('Key niet gevonden (key, userid, category)', key, userid, category)

    # def get_category(self, userid, category):
    #     try:
    #         value = self._cache[userid][category]
    #         return value
    #     except:
    #         return None

    # def get_user(self, userid):
    #     try:
    #         value = self._cache[userid]
    #         return value
    #     except:
    #         return None

    def set(self, key, value, **kwargs):
        userid = kwargs.get('userid')
        category = kwargs.get('category')

        if not userid:
            self._cache['global'][key] = value
        elif category:
            try:
                self._cache[userid][category][key] = value
            except:
                try:
                    self._cache[userid][category] = {key: value}
                except:
                    self._cache[userid] = {category: { key: value }}
        else:
            print('Geen route gevonden (key, value, userid, category)', key, value, userid, category)

    def delete(self, **kwargs):
        key = kwargs.get('key')
        userid = kwargs.get('userid')
        category = kwargs.get('category')

        if not userid and key:
            self._cache['global'].pop(key)
        elif userid and category and key:
            try:
                self._cache[userid][category].pop(key, None)
            except:
                print('Bestond al niet')
        elif userid and category:
            try:
                self._cache[userid].pop(category, None)
            except:
                print('Bestond al niet')
        elif userid:
            self._cache.pop(userid, None)
        else:
            print('Geen route gevonden (key, userid, category)', key, userid, category)
    
    # def set_global(self, key, value):
    #     self._cache['global'][key] = value

    # def get_global(self, key):
    #     try:
    #         return self._cache['global'][key]
    #     except:
    #         return None

    # def delete_global(self, key):
    #     try:
    #         self._cache['global'].pop(key, None)
    #     except:
    #         pass

    # def delete_user(self, userid):
    #     self._cache.pop(userid, None)

    # def delete_category(self, userid, category):
    #     try:
    #         self._cache[userid].pop(category, None)
    #     except:
    #         print('Bestond al niet')

    # def delete_key(self, userid, category, key):
    #     try:
    #         self._cache[userid][category].pop(key, None)
    #     except:
    #         print('Bestond al niet')



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
