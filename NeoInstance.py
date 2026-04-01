from neo4j import GraphDatabase

class NeoInstance:

    def __init__(self, ip, username, password):
        self.instanceInfo = {"URI" : f"neo4j://{ip}", "AUTH" : (username, password)}
        print(self.instanceInfo['AUTH'])
        print("Connecting to neo4j Instance...")
        self.driver = GraphDatabase.driver(self.instanceInfo['URI'], auth=self.instanceInfo['AUTH'])
        try :
            self.driver.verify_connectivity()
            print("Connection OK !")
            self.driver.verify_authentication()
            print("AUTH OK !")
        except:
            raise Exception("NeoInstance Connection/AUTH Error")
        


    def req(self, query):
        records, summary, keys = self.driver.execute_query(query, database_="neo4j")
        result = [record.data() for record in records]
        return result
    
    def close(self):
        self.driver.close()