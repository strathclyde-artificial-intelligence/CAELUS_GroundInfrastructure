import sqlite3

class DBAdapter():
    """
    Connect to a local sqlite database.
    """
    def __init__(self, db_path = None):
        # if db_path is None create a in-memory database
        if db_path is None:
            self.db_path = ":memory:"
        else:
            self.db_path = db_path
        self.setup()

    def setup(self):
        """
        Setup the database.
        Create a table if it doesn't exist for Drones
        Drones should contain:
            - id
            - type
            - state
            - reservation_token
            - mission_id
            - mission json
            - config_name
        """
        self.__connect()
        self.__execute("""
            CREATE TABLE IF NOT EXISTS Drones (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                state TEXT NOT NULL,
                reservation_token TEXT,
                mission_id TEXT,
                mission_json TEXT,
                config_name TEXT NOT NULL
            )
        """)

    def get_drones(self):
        """
        Get all the drones from the database.
        """
        self.__execute("SELECT * FROM Drones")
        return self.__fetchall()

    def __connect(self):
        """
        Connect to the database.
        """
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def __disconnect(self):
        """
        Disconnect from the database.
        """
        self.conn.close()

    def __execute(self, query, params=None):
        """
        Execute a query on the database.
        """
        if params is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        self.conn.commit()

    def add_or_edit_drone(self, drone):
        """
        Add or edit a drone in the database.
        """
        self.__execute("""
            INSERT OR REPLACE INTO Drones
            (id, type, state, reservation_token, mission_id, mission_json, config_name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, drone.to_sqlite())

    def get_drone_state(self, drone_id):
        """
        Get the state of a drone.
        """
        self.__execute("SELECT state FROM Drones WHERE id=?", (drone_id,))
        return self.__fetchone()[0]

    def remove_drone_if_exists(self, drone_id):
        """
        Remove a drone from the database if it exists.
        """
        self.__execute("DELETE FROM Drones WHERE id=?", (drone_id,))

    def __fetchall(self):
        """
        Fetch all the rows of the last query.
        """
        return self.cursor.fetchall()

    def __fetchone(self):
        """
        Fetch one row of the last query.
        """
        return self.cursor.fetchone()

    def __fetchmany(self, size=10):
        """
        Fetch multiple rows of the last query.
        """
        return self.cursor.fetchmany(size)

# Create a mock version of the DBAdapter
# Every operation is performed in-memory.
class MockDBAdapter(DBAdapter):
    """
    A mock DBAdapter.
    """
    def __init__(self):
        self.drones = []

    def setup(self):
        """
        Setup the database.
        Create a table if it doesn't exist for Drones
        Drones should contain:
            - id
            - state
            - reservation_token
            - mission_id
            - mission json
        """
        pass

    def get_drones(self):
        """
        Get all the drones from the database.
        """
        return self.drones

    def add_or_edit_drone(self, drone):
        """
        Add or edit a drone in the database.
        """
        self.drones.append(drone)

    def remove_drone_if_exists(self, drone_id):
        """
        Remove a drone from the database if it exists.
        """
        self.drones = [drone for drone in self.drones if drone.get_drone_id() != drone_id]
