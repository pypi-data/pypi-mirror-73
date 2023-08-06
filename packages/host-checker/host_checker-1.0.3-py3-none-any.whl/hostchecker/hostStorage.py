from hostingInfo import HostInfo
import sqlite3

from dataclasses import dataclass

@dataclass
class HostStat:
    percentage: float
    count: int
    datacenter: str


class HostStorage:
    def __init__(self, name):
        """
        :param name: Name of the db or path
        """
        self._conn = sqlite3.connect(name)
        self._conn.execute("CREATE table if not EXISTS hosts (domain text PRIMARY KEY, datacenter text)")
        self._conn.commit()

    def getHostInfo(self, domain):
        """
        Obtains the datacener of a given domain

        :param domain: Domain to fetch
        :return: Datacenter
        """
        rows = self._conn.execute("SELECT * FROM hosts WHERE domain=?", (domain,))

        for (domain, datacenter) in rows.fetchall():
            return HostInfo(domain=domain, datacenter=datacenter)

        return None

    def cache(self, hostsInfo):
        """
        Cache the given data

        :param hostInfo: A list of HostInfo to store
        """

        rows = []
        for h in hostsInfo:
            rows.append((h.domain, h.datacenter))

        self._conn.executemany("INSERT OR REPLACE INTO hosts (domain, datacenter) VALUES (?,?)", rows)
        self._conn.commit()

    def stats(self):
        """
        Get stats from the cached values

        :return: HostStat
        """

        rows = self._conn.execute("""
            SELECT datacenter, count(*) AS NumOcc
            FROM hosts
            GROUP BY datacenter
            ORDER BY Numocc asc
            """)

        numTot = self._conn.execute("SELECT COUNT(*) FROM hosts").fetchone()[0]

        result = []
        for (datacenter, numOcc) in rows.fetchall():
            result.append(HostStat(numOcc / numTot, numOcc, datacenter))


        return result

