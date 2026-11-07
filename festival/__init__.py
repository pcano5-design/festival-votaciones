import pymysql

# Django 5.2 pide que el conector se identifique como versión 2.2.1 o superior.
# PyMySQL funciona bien, pero se identifica con un número antiguo; esta línea lo corrige.
pymysql.version_info = (2, 2, 1, "final", 0)

pymysql.install_as_MySQLdb()