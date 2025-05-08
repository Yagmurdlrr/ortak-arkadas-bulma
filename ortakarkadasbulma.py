# Bu modül, arkadaşlık ilişkilerini yönetmek için HashTable veri yapısını ve
# ortak arkadaşları bulmak için gerekli fonksiyonları içerir.

class HashTable:
    def __init__(self):
        
        self.table = {}

    def insert(self, key, value):
       
      
        if not isinstance(key, str):
            raise ValueError('Key değeri mutlaka string olmalı.')

       
        if not isinstance(value, list):
            raise ValueError('Value değeri mutlaka liste olmalı.')

        self.table[key] = value

    def get(self, key):
       
        if not isinstance(key, str):
            raise ValueError('Key değeri mutlaka string olmalı.')

        return self.table.get(key, None)

friendship_table = HashTable()

def find_common_friends(user1, user2, hashtable):
  
    if not isinstance(user1, str) or not isinstance(user2, str):
        raise ValueError('Kullanıcı adı mutlaka string olmalı.')

    
    friends_user1 = set(hashtable.get(user1) or []) 
    friends_user2 = set(hashtable.get(user2) or []) 

    if not friends_user1:
        print(f"Hata: '{user1}' kullanıcı bulunamadı.")

    if not friends_user2:
        print(f"Hata: '{user2}' kullanıcı bulunamadı.")

    common_friends = friends_user1.intersection(friends_user2)

    return list(common_friends)


