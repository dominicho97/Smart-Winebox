from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    # alle metingen

    @staticmethod
    def read_alle_metingen(sensor_id):
        sql = "SELECT * from metingen WHERE sensorid = %s ORDER BY startDatum DESC"
        params = [sensor_id]
        return Database.get_rows(sql, params)


#   vochtigheid (enkel 1(huidige) rij opvragen)

    @staticmethod
    def read_vochtigheid():
        sql = "SELECT gemetenWaarde FROM metingen WHERE sensorId = 1 ORDER BY startDatum DESC"
        return Database.get_one_row(sql)

    @staticmethod
    def create_vochtigheid(sensorid, gemetenWaarde, startDatum, eindDatum):
        sql = "INSERT INTO metingen  (SensorId, GemetenWaarde, StartDatum, EindDatum) VALUES (%s,%s,%s,%s)"
        params = [sensorid, gemetenWaarde, startDatum, eindDatum]
        return Database.execute_sql(sql, params)
# VolgNummer,SensorId, GemetenWaarde

#   temperatuur

    @staticmethod
    def read_temperatuur():
        sql = "SELECT  gemetenWaarde FROM metingen WHERE sensorId = 2 ORDER BY startDatum DESC"
        return Database.get_one_row(sql)

    # alle rijene ipv 1 rij om te testen
    @staticmethod
    def read_alle_temperaturen():
        sql = "SELECT  gemetenWaarde FROM metingen WHERE sensorId = 2 ORDER BY startDatum DESC"
        return Database.get_rows(sql)

    @staticmethod
    def create_temperatuur(sensorid, gemetenWaarde, startDatum, eindDatum):
        sql = "INSERT INTO metingen  (SensorId, GemetenWaarde, StartDatum, EindDatum) VALUES (%s,%s,%s,%s)"
        params = [sensorid, gemetenWaarde, startDatum, eindDatum]
        return Database.execute_sql(sql, params)


#   licht


    @staticmethod
    def read_licht():
        sql = "SELECT gemetenWaarde FROM metingen WHERE sensorId = 3 ORDER By startDatum DESC"
        return Database.get_one_row(sql)

    @staticmethod
    def create_licht(sensorid, gemetenWaarde, startDatum, eindDatum):
        sql = "INSERT INTO metingen  (SensorId, GemetenWaarde, StartDatum, EindDatum) VALUES (%s, %s,%s,%s)"
        params = [sensorid, gemetenWaarde, startDatum, eindDatum]
        return Database.execute_sql(sql, params)
