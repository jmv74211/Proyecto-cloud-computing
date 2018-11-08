### Test en python con Unittest

---

- En primer lugar hay que importar el módulo unittest: `import unittest`

- Se crea un archivo denominado **test_x.py** que contendrá las pruebas del módulo x.

- Se crea una clase llamada TestX(unittest.TestCase) donde x es el nombre del módulo. Dentro de dicha clase se crearán los métodos de pruebas.

- Los métodos de pruebas deben de seguir la convencion `def test_x(self)` donde x es el nombre de la funcionalidad que va a testear este método.

- Debajo de la clase de TestX, hay que añadir la línea para que se ejecuten todos los test al usar `python test_x.py`

      if __name__ == '__main__':
         unittest.main()
- Las comprobaciones las podemos hacer con asserts: **[enlace](https://docs.python.org/3/library/unittest.html)**

|Method | Checks that |	New in |
|assertEqual(a, b) | 	a == b |	|
|assertTrue(x)  |	bool(x) is True ||
|assertNotEqual(a, b) |	a != b 	||
|assertFalse(x) |	bool(x) is False ||	 
|assertIs(a, b) |	a is b |	3.1|
|assertIsNot(a, b) |	a is not b |3.1|
|assertIsNone(x) |	x is None |	3.1 |
|assertIsNotNone(x) | 	x is not None | 3.1|
|assertIn(a, b) |	a in b | 3.1 |
|assertNotIn(a, b) |	a not in b | 3.1 |
|assertIsInstance(a, b) |	isinstance(a, b) | 3.2|
|assertNotIsInstance(a, b) |	not isinstance(a, b) | 	3.2 |

- Para comprobar si se ejecutan las excepciones programadas dentro de los métodos de las funciones, podemos utiizar `assertRaises`. por ejemplo:

      self.assertRaises(tipoError, nombreMetodo, parametro1, parametro2...)

   o
      with self.assertRaises(tipoError):
         nombreMetodo(parametro1,parametro2...)

- El método `def setUp(self)` se ejecutará antes de cada test

- El método `def tearDown(self)` se ejecutará despues de cada test

- Estos dos métodos anteriores tienen el objetivo de declarar e inicializar las variables que se ven a utilizar en cada método sin la necesidad de decalarar y repetir las mismas variables para cada método.
Es importante que el las variables se declaren **self.variable** dentro de estos métodos.

- En el caso de que solo se quieran ejecutar una vez en todo el conjunto de los test, se deberán de declarar de la siguiente forma:

         @classmethod
         def setUpClass(cls):
            print('setupClass')

         @classmethod
         def tearDownClass(cls):
            print('tearDownClass')

Es importante saber que la utilidad de los test es comprobar si nuestro código funciona. En el caso de que nosotros ejecutáramos nuestros test en un servidor caído, los test fallarían, pero no debido a nuestro código, sino al servidor. Para evitar esto, vamos a comprobar el estado del servidor antes de ejecutar los test.
```
