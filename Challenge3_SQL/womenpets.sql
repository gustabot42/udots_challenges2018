/*
Write the SQL statement that shows the name of the women who have pets in Bogotá.
using database file 'db.sqlite3'
*/

SELECT c.Nombre
FROM Clientes AS c
INNER JOIN Datos AS g ON c.ClienteID = g.Cliente
INNER JOIN Datos AS m ON c.ClienteID = m.Cliente
INNER JOIN Datos AS l ON c.ClienteID = l.Cliente
WHERE g.Variable = 'Genero'  AND g.Valor = 'F'
  AND m.Variable = 'Mascota' AND m.Valor = 'Si'
  AND l.Variable = 'Ciudad'  AND l.Valor = 'Bogota'

/*
Name of the women who have pets in Bogotá.
"Maria"

Name of the women who have pets
"Maria", "Catalina"

Name of the women
"Maria", "Diana", "Cata"
*/
