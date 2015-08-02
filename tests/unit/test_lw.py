from caspy import lw


class TestGet:
    def setup(self):
        class Ob:
            pass
        self.a = Ob()
        self.a.color = 'crimson'
        self.b = Ob()
        self.b.color = 'blue'
        self.b.size = 2

    def test_get_obj_attr(self):
        assert lw.get('color', self.a) == 'crimson'

    def test_get_missing_attr(self):
        assert lw.get('size', self.a) is None

    def test_fallback_obj(self):
        assert lw.get('color', self.a, self.b) == 'crimson'
        assert lw.get('size', self.a, self.b) == 2

    def test_fallback_kwargs(self):
        assert lw.get('color', self.a, self.b, shape='square') == 'crimson'
        assert lw.get('size', self.a, self.b, shape='square') == 2
        assert lw.get('shape', self.a, self.b, shape='square') == 'square'

    def test_kwarg_override(self):
        assert lw.get('color', self.b, color='maize') == 'maize'


class TestLightweight:
    class Polygon(lw.Lightweight):
        _fields = 'sides', 'size'

    def setup(self):
        self.u_square = self.Polygon(sides=4, size=1)

    def test_init(self):
        assert self.u_square.sides == 4
        assert self.u_square.size == 1
        u_triangle = self.Polygon(self.u_square, sides=3)
        assert u_triangle.sides == 3
        assert u_triangle.size == 1

    def test_init_copy(self):
        obj = self.Polygon(self.u_square)
        assert obj.sides == 4
        assert obj.size == 1

    def test_init_dict(self):
        obj = self.Polygon({'sides': 4, 'size': 1})
        assert obj.sides == 4
        assert obj.size == 1

    def test_init_from_obj(self):
        class TestClass:
            sides = 8
            size = 2
        obj = self.Polygon(TestClass())
        assert obj.sides == 8
        assert obj.size == 2

    def test_copy(self):
        self.u_square = self.Polygon(sides=4, size=1)
        u_pent = self.u_square.copy(sides=5)
        assert u_pent.sides == 5
        assert u_pent.size == 1

    def test_str(self):
        assert str(self.u_square) == '4'

    def test_repr(self):
        assert repr(self.u_square) == 'Polygon(sides=4, size=1)'
        o = self.Polygon(size='Big!')
        assert repr(o) == "Polygon(sides=None, size='Big!')"

    def test_attr_named_name(self):
        class Obj(lw.Lightweight):
            _fields = 'name',
        o = Obj(name='Bob')
        assert repr(o) == "Obj(name='Bob')"

    def test_dict(self):
        assert dict(self.u_square) == {'sides': 4, 'size': 1}

    def test_doublestar(self):
        assert dict(**self.u_square) == {'sides': 4, 'size': 1}
