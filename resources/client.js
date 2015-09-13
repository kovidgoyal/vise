(function(){
    "use strict;";
    var _$rapyd$_iterator_symbol = (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") ? Symbol.iterator : "iterator-Symbol-5d0927e5554349048cf0e3762a228256";
    var _$rapyd$_kwargs_symbol = (typeof Symbol === "function") ? Symbol("kwargs-object") : "kwargs-object-Symbol-5d0927e5554349048cf0e3762a228256";
    var _$rapyd$_cond_temp;
    var _$rapyd$_in = (function _$rapyd$_in() {
            if (typeof Map === "function" && typeof Set === "function") {
                return function(val, arr) {
                    if (Array.isArray(arr) || typeof arr === "string") {
                        return arr.indexOf(val) !== -1;
                    }
                    if (typeof arr.__contains__ === "function") {
                        return arr.__contains__(val);
                    }
                    if ((arr instanceof Map || arr instanceof Set)) {
                        return arr.has(val);
                    }
                    return arr.hasOwnProperty(val);
                };
            }
            return function(val, arr) {
                if (Array.isArray(arr) || typeof arr === "string") {
                    return arr.indexOf(val) !== -1;
                }
                if (typeof arr.__contains__ === "function") {
                    return arr.__contains__(val);
                }
                return arr.hasOwnProperty(val);
            };
        })();
    function _$rapyd$_Iterable(iterable) {
            var iterator, ans, result;
            if (Array.isArray(iterable) || typeof iterable === "string") {
                return iterable;
            }
            if (typeof iterable[_$rapyd$_iterator_symbol] === "function") {
                iterator = (typeof Map === "function" && iterable instanceof Map) ? iterable.keys() : iterable[_$rapyd$_iterator_symbol]();
                ans = _$rapyd$_list_decorate([]);
                result = iterator.next();
                while (!result.done) {
                    ans.push(result.value);
                    result = iterator.next();
                }
                return ans;
            }
            if (typeof HTMLCollection === "function" && (iterable instanceof HTMLCollection || iterable instanceof NodeList || iterable instanceof NamedNodeMap)) {
                return iterable;
            }
            return Object.keys(iterable);
        }
    var _$rapyd$_desugar_kwargs = (function _$rapyd$_desugar_kwargs() {
            if (typeof Object.assign === "function") {
                return function() {
                    var ans;
                    ans = {};
                    ans[_$rapyd$_kwargs_symbol] = true;
                    return Object.assign.apply(ans, arguments);
                };
            }
            return function() {
                var ans, keys;
                ans = {};
                ans[_$rapyd$_kwargs_symbol] = true;
                for (var i = 0; i < arguments.length; i++) {
                    keys = Object.keys(arguments[i]);
                    for (var j = 0; j < keys.length; j++) {
                        ans[keys[j]] = arguments[i][keys[j]];
                    }
                }
                return ans;
            };
        })();
    var Exception = Error;
function AttributeError() {
    AttributeError.prototype.__init__.apply(this, arguments);
}
_$rapyd$_extends(AttributeError, Error);
AttributeError.prototype.__init__ = function __init__(msg) {
    var self = this;
    self.message = msg;
    self.stack = new Error().stack;
};
AttributeError.prototype.name = "AttributeError";

function IndexError() {
    IndexError.prototype.__init__.apply(this, arguments);
}
_$rapyd$_extends(IndexError, Error);
IndexError.prototype.__init__ = function __init__(msg) {
    var self = this;
    self.message = msg;
    self.stack = new Error().stack;
};
IndexError.prototype.name = "IndexError";

function KeyError() {
    KeyError.prototype.__init__.apply(this, arguments);
}
_$rapyd$_extends(KeyError, Error);
KeyError.prototype.__init__ = function __init__(msg) {
    var self = this;
    self.message = msg;
    self.stack = new Error().stack;
};
KeyError.prototype.name = "KeyError";

function ValueError() {
    ValueError.prototype.__init__.apply(this, arguments);
}
_$rapyd$_extends(ValueError, Error);
ValueError.prototype.__init__ = function __init__(msg) {
    var self = this;
    self.message = msg;
    self.stack = new Error().stack;
};
ValueError.prototype.name = "ValueError";

    function _$rapyd$_equals(a, b) {
    try {
        return a.__eq__(b);
    } catch (_$rapyd$_Exception) {
        if (_$rapyd$_Exception instanceof TypeError) {
            return a === b;
        } else {
            throw _$rapyd$_Exception;
        }
    }
}
"var equals = _$rapyd$_equals";
function _$rapyd$_list_extend(iterable) {
    var start, iterator, result;
    if (Array.isArray(iterable) || typeof iterable === "string") {
        start = this.length;
        this.length += iterable.length;
        for (var i = 0; i < iterable.length; i++) {
            this[start + i] = iterable[i];
        }
    } else {
        iterator = (typeof Map === "function" && iterable instanceof Map) ? iterable.keys() : iterable[_$rapyd$_iterator_symbol]();
        result = iterator.next();
        while (!result.done) {
            this.push(result.value);
            result = iterator.next();
        }
    }
}
function _$rapyd$_list_index(val, start, stop) {
    var idx;
    start = start || 0;
    if (start < 0) {
        start = this.length + start;
    }
    if (start < 0) {
        throw new ValueError(val + " is not in list");
    }
    if (stop === undefined) {
        idx = this.indexOf(val, start);
        if (idx === -1) {
            throw new ValueError(val + " is not in list");
        }
        return idx;
    }
    if (stop < 0) {
        stop = this.length + stop;
    }
    for (var i = start; i < stop; i++) {
        if (this[i] === val) {
            return i;
        }
    }
    throw new ValueError(val + " is not in list");
}
function _$rapyd$_list_pop(index) {
    var ans;
    if (this.length === 0) {
        throw new IndexError("list is empty");
    }
    ans = this.splice(index, 1);
    if (!ans.length) {
        throw new IndexError("pop index out of range");
    }
    return ans[0];
}
function _$rapyd$_list_remove(value) {
    var idx;
    idx = this.indexOf(value);
    if (idx === -1) {
        throw new ValueError(value + " not in list");
    }
    this.splice(idx, 1);
}
function _$rapyd$_list_to_string() {
    return "[" + this.join(", ") + "]";
}
function _$rapyd$_list_insert(index, val) {
    if (index < 0) {
        index += this.length;
    }
    index = min(this.length, max(index, 0));
    if (index === 0) {
        this.unshift(val);
        return;
    }
    for (var i = this.length; i > index; i--) {
        this[i] = this[i - 1];
    }
    this[index] = val;
}
function _$rapyd$_list_copy() {
    return _$rapyd$_list_constructor(this);
}
function _$rapyd$_list_clear() {
    this.length = 0;
}
function _$rapyd$_list_as_array() {
    return Array.prototype.slice.call(this);
}
function _$rapyd$_list_count(value) {
    return this.reduce(function(n, val) {
        return n + (val === value);
    }, 0);
}
function _$rapyd$_list_sort_key(value) {
    var t;
    t = typeof value;
    if (t === "string" || t === "number") {
        return value;
    }
    return value.toString();
}
function _$rapyd$_list_sort_cmp(a, b) {
    if (a < b) {
        return -1;
    }
    if (a > b) {
        return 1;
    }
    return 0;
}
function _$rapyd$_list_sort() {
    var key = (arguments[0] === undefined || ( 0 === arguments.length-1 && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [_$rapyd$_kwargs_symbol] === true)) ? (null) : arguments[0];
    var reverse = (arguments[1] === undefined || ( 1 === arguments.length-1 && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [_$rapyd$_kwargs_symbol] === true)) ? (false) : arguments[1];
    var _$rapyd$_kwargs_obj = arguments[arguments.length-1];
    if (typeof _$rapyd$_kwargs_obj !== "object" || _$rapyd$_kwargs_obj [_$rapyd$_kwargs_symbol] !== true) _$rapyd$_kwargs_obj = {};
    if (Object.prototype.hasOwnProperty.call(_$rapyd$_kwargs_obj, "key")){
        key = _$rapyd$_kwargs_obj.key;
    }
    if (Object.prototype.hasOwnProperty.call(_$rapyd$_kwargs_obj, "reverse")){
        reverse = _$rapyd$_kwargs_obj.reverse;
    }
    var mult, keymap, k;
    key = key || _$rapyd$_list_sort_key;
    mult = (reverse) ? -1 : 1;
    keymap = dict();
    for (var i=0; i < this.length; i++) {
        k = this[i];
        keymap.set(k, key(k));
    }
    this.sort(function(a, b) {
        return mult * _$rapyd$_list_sort_cmp(keymap.get(a), keymap.get(b));
    });
}
function _$rapyd$_list_concat() {
    var ans;
    ans = Array.prototype.concat.apply(this, arguments);
    _$rapyd$_list_decorate(ans);
    return ans;
}
function _$rapyd$_list_slice() {
    var ans;
    ans = Array.prototype.slice.apply(this, arguments);
    _$rapyd$_list_decorate(ans);
    return ans;
}
function _$rapyd$_list_iterator(value) {
    var self;
    self = this;
    return {
        "_i": -1,
        "_list": self,
        "next": function() {
            this._i += 1;
            if (this._i >= this._list.length) {
                return {
                    "done": true
                };
            }
            return {
                "done": false,
                "value": this._list[this._i]
            };
        }
    };
}
function _$rapyd$_list_len() {
    return this.length;
}
function _$rapyd$_list_contains(val) {
    return this.indexOf(val) !== -1;
}
function _$rapyd$_list_eq(other) {
    if (!Array.isArray(other)) {
        return false;
    }
    if (other.length !== this.length) {
        return false;
    }
    if (other.length === 0) {
        return true;
    }
    for (var i = 0; i < other.length; i++) {
        if (!_$rapyd$_equals(this[i], other[i])) {
            return false;
        }
    }
    return true;
}
function _$rapyd$_list_decorate(ans) {
    ans.append = Array.prototype.push;
    ans.toString = _$rapyd$_list_to_string;
    ans.inspect = _$rapyd$_list_to_string;
    ans.extend = _$rapyd$_list_extend;
    ans.index = _$rapyd$_list_index;
    ans.pypop = _$rapyd$_list_pop;
    ans.remove = _$rapyd$_list_remove;
    ans.insert = _$rapyd$_list_insert;
    ans.copy = _$rapyd$_list_copy;
    ans.clear = _$rapyd$_list_clear;
    ans.count = _$rapyd$_list_count;
    ans.concat = _$rapyd$_list_concat;
    ans.pysort = _$rapyd$_list_sort;
    ans.slice = _$rapyd$_list_slice;
    ans.as_array = _$rapyd$_list_as_array;
    ans.__len__ = _$rapyd$_list_len;
    ans.__contains__ = _$rapyd$_list_contains;
    ans.__eq__ = _$rapyd$_list_eq;
    ans.constructor = _$rapyd$_list_constructor;
    if (typeof ans[_$rapyd$_iterator_symbol] !== "function") {
        ans[_$rapyd$_iterator_symbol] = _$rapyd$_list_iterator;
    }
    return ans;
}
function _$rapyd$_list_constructor(iterable) {
    var ans, iterator, result;
    if (iterable === undefined) {
        ans = [];
    } else if (Array.isArray(iterable) || typeof iterable === "string") {
        ans = new Array(iterable.length);
        for (var i = 0; i < iterable.length; i++) {
            ans[i] = iterable[i];
        }
    } else if (typeof iterable[_$rapyd$_iterator_symbol] === "function") {
        iterator = (typeof Map === "function" && iterable instanceof Map) ? iterable.keys() : iterable[_$rapyd$_iterator_symbol]();
        ans = _$rapyd$_list_decorate([]);
        result = iterator.next();
        while (!result.done) {
            ans.push(result.value);
            result = iterator.next();
        }
    } else if (typeof iterable === "number") {
        ans = new Array(iterable);
    } else {
        ans = Object.keys(iterable);
    }
    return _$rapyd$_list_decorate(ans);
}
_$rapyd$_list_constructor.__name__ = "list";
var list = _$rapyd$_list_constructor, list_wrap = _$rapyd$_list_decorate;
var _$rapyd$_global_object_id = 0, _$rapyd$_set_implementation;
function _$rapyd$_set_keyfor(x) {
    var t, ans;
    t = typeof x;
    if (t === "string" || t === "number" || t === "boolean") {
        return "_" + t[0] + x;
    }
    if (x == null) {
        return "__!@#$0";
    }
    ans = x._$rapyd$_hash_key_prop;
    if (ans === undefined) {
        ans = "_!@#$" + ++_$rapyd$_global_object_id;
        Object.defineProperty(x, "_$rapyd$_hash_key_prop", {
            "value": ans
        });
    }
    return ans;
}
function _$rapyd$_set_polyfill() {
    this._store = {};
    this.size = 0;
}
_$rapyd$_set_polyfill.prototype.add = function(x) {
    var key;
    key = _$rapyd$_set_keyfor(x);
    if (!Object.hasOwnProperty.call(this._store, key)) {
        this.size += 1;
        this._store[key] = x;
    }
    return this;
};
_$rapyd$_set_polyfill.prototype.clear = function(x) {
    this._store = {};
    this.size = 0;
};
_$rapyd$_set_polyfill.prototype.delete = function(x) {
    var key;
    key = _$rapyd$_set_keyfor(x);
    if (Object.hasOwnProperty.call(this._store, key)) {
        this.size -= 1;
        delete this._store[key];
        return true;
    }
    return false;
};
_$rapyd$_set_polyfill.prototype.has = function(x) {
    return Object.hasOwnProperty.call(this._store, _$rapyd$_set_keyfor(x));
};
_$rapyd$_set_polyfill.prototype.values = function(x) {
    var keys, s;
    keys = Object.keys(this._store);
    s = this._store;
    return (function(){
        var _$rapyd$_d = {};
        _$rapyd$_d["_keys"] = keys;
        _$rapyd$_d["_i"] = -1;
        _$rapyd$_d["_s"] = s;
        _$rapyd$_d[_$rapyd$_iterator_symbol] = function() {
            return this;
        };
        _$rapyd$_d["next"] = function() {
            this._i += 1;
            if (this._i >= this._keys.length) {
                return {
                    "done": true
                };
            }
            return {
                "done": false,
                "value": s[this._keys[this._i]]
            };
        };
        return _$rapyd$_d;
    })();
};
if (typeof Set !== "function" || typeof Set.prototype.delete !== "function") {
    _$rapyd$_set_implementation = _$rapyd$_set_polyfill;
} else {
    _$rapyd$_set_implementation = Set;
}
function _$rapyd$_set(iterable) {
    var ans, s, iterator, result, keys;
    if (this instanceof _$rapyd$_set) {
        this.jsset = new _$rapyd$_set_implementation();
        ans = this;
        if (iterable === undefined) {
            return ans;
        }
        s = ans.jsset;
        if (Array.isArray(iterable) || typeof iterable === "string") {
            for (var i = 0; i < iterable.length; i++) {
                s.add(iterable[i]);
            }
        } else if (typeof iterable[_$rapyd$_iterator_symbol] === "function") {
            iterator = (typeof Map === "function" && iterable instanceof Map) ? iterable.keys() : iterable[_$rapyd$_iterator_symbol]();
            result = iterator.next();
            while (!result.done) {
                s.add(result.value);
                result = iterator.next();
            }
        } else {
            keys = Object.keys(iterable);
            for (var i=0; i < keys.length; i++) {
                s.add(keys[i]);
            }
        }
        return ans;
    } else {
        return new _$rapyd$_set(iterable);
    }
}
_$rapyd$_set.prototype.__name__ = "set";
Object.defineProperties(_$rapyd$_set.prototype, {
    "length": {
        "get": function() {
            return this.jsset.size;
        }
    },
    "size": {
        "get": function() {
            return this.jsset.size;
        }
    }
});
_$rapyd$_set.prototype.__len__ = function() {
    return this.jsset.size;
};
_$rapyd$_set.prototype.has = _$rapyd$_set.prototype.__contains__ = function(x) {
    return this.jsset.has(x);
};
_$rapyd$_set.prototype.add = function(x) {
    this.jsset.add(x);
};
_$rapyd$_set.prototype.clear = function() {
    this.jsset.clear();
};
_$rapyd$_set.prototype.copy = function() {
    return _$rapyd$_set(this);
};
_$rapyd$_set.prototype.discard = function(x) {
    this.jsset.delete(x);
};
_$rapyd$_set.prototype[_$rapyd$_iterator_symbol] = function() {
    return this.jsset.values();
};
_$rapyd$_set.prototype.difference = function() {
    var ans, s, iterator, r, x, has;
    ans = new _$rapyd$_set();
    s = ans.jsset;
    iterator = this.jsset.values();
    r = iterator.next();
    while (!r.done) {
        x = r.value;
        has = false;
        for (var i = 0; i < arguments.length; i++) {
            if (arguments[i].has(x)) {
                has = true;
                break;
            }
        }
        if (!has) {
            s.add(x);
        }
        r = iterator.next();
    }
    return ans;
};
_$rapyd$_set.prototype.difference_update = function() {
    var s, remove, iterator, r, x;
    s = this.jsset;
    remove = [];
    iterator = s.values();
    r = iterator.next();
    while (!r.done) {
        x = r.value;
        for (var i = 0; i < arguments.length; i++) {
            if (arguments[i].has(x)) {
                remove.push(x);
                break;
            }
        }
        r = iterator.next();
    }
    for (var i = 0; i < remove.length; i++) {
        s.delete(remove[i]);
    }
};
_$rapyd$_set.prototype.intersection = function() {
    var ans, s, iterator, r, x, has;
    ans = new _$rapyd$_set();
    s = ans.jsset;
    iterator = this.jsset.values();
    r = iterator.next();
    while (!r.done) {
        x = r.value;
        has = true;
        for (var i = 0; i < arguments.length; i++) {
            if (!arguments[i].has(x)) {
                has = false;
                break;
            }
        }
        if (has) {
            s.add(x);
        }
        r = iterator.next();
    }
    return ans;
};
_$rapyd$_set.prototype.intersection_update = function() {
    var s, remove, iterator, r, x;
    s = this.jsset;
    remove = [];
    iterator = s.values();
    r = iterator.next();
    while (!r.done) {
        x = r.value;
        for (var i = 0; i < arguments.length; i++) {
            if (!arguments[i].has(x)) {
                remove.push(x);
                break;
            }
        }
        r = iterator.next();
    }
    for (var i = 0; i < remove.length; i++) {
        s.delete(remove[i]);
    }
};
_$rapyd$_set.prototype.isdisjoint = function(other) {
    var iterator, r, x;
    iterator = this.jsset.values();
    r = iterator.next();
    while (!r.done) {
        x = r.value;
        if (other.has(x)) {
            return false;
        }
        r = iterator.next();
    }
    return true;
};
_$rapyd$_set.prototype.issubset = function(other) {
    var iterator, r, x;
    iterator = this.jsset.values();
    r = iterator.next();
    while (!r.done) {
        x = r.value;
        if (!other.has(x)) {
            return false;
        }
        r = iterator.next();
    }
    return true;
};
_$rapyd$_set.prototype.issuperset = function(other) {
    var s, iterator, r, x;
    s = this.jsset;
    iterator = other.jsset.values();
    r = iterator.next();
    while (!r.done) {
        x = r.value;
        if (!s.has(x)) {
            return false;
        }
        r = iterator.next();
    }
    return true;
};
_$rapyd$_set.prototype.pop = function() {
    var iterator, r;
    iterator = this.jsset.values();
    r = iterator.next();
    if (r.done) {
        throw new KeyError("pop from an empty set");
    }
    this.jsset.delete(r.value);
    return r.value;
};
_$rapyd$_set.prototype.remove = function(x) {
    if (!this.jsset.delete(x)) {
        throw new KeyError(x.toString());
    }
};
_$rapyd$_set.prototype.symmetric_difference = function(other) {
    return this.union(other).difference(this.intersection(other));
};
_$rapyd$_set.prototype.symmetric_difference_update = function(other) {
    var common;
    common = this.intersection(other);
    this.update(other);
    this.difference_update(common);
};
_$rapyd$_set.prototype.union = function() {
    var ans;
    ans = _$rapyd$_set(this);
    ans.update.apply(ans, arguments);
    return ans;
};
_$rapyd$_set.prototype.update = function() {
    var s, iterator, r;
    s = this.jsset;
    for (var i=0; i < arguments.length; i++) {
        iterator = arguments[i][_$rapyd$_iterator_symbol]();
        r = iterator.next();
        while (!r.done) {
            s.add(r.value);
            r = iterator.next();
        }
    }
};
_$rapyd$_set.prototype.toString = _$rapyd$_set.prototype.inspect = function() {
    return "{" + list(this).join(", ") + "}";
};
_$rapyd$_set.prototype.__eq__ = function(other) {
    var iterator, r;
    if (!(other instanceof this.constructor)) {
        return false;
    }
    if (other.size !== this.size) {
        return false;
    }
    if (other.size === 0) {
        return true;
    }
    iterator = other[_$rapyd$_iterator_symbol]();
    r = iterator.next();
    while (!r.done) {
        if (!this.has(r.value)) {
            return false;
        }
        r = iterator.next();
    }
    return true;
};
function _$rapyd$_set_wrap(x) {
    var ans;
    ans = new _$rapyd$_set();
    ans.jsset = x;
    return ans;
}
var set = _$rapyd$_set, set_wrap = _$rapyd$_set_wrap;
var _$rapyd$_dict_implementation;
function _$rapyd$_dict_polyfill() {
    this._store = {};
    this.size = 0;
}
_$rapyd$_dict_polyfill.prototype.set = function(x, value) {
    var key;
    key = _$rapyd$_set_keyfor(x);
    if (!Object.hasOwnProperty.call(this._store, key)) {
        this.size += 1;
    }
    this._store[key] = [x, value];
    return this;
};
_$rapyd$_dict_polyfill.prototype.clear = function(x) {
    this._store = {};
    this.size = 0;
};
_$rapyd$_dict_polyfill.prototype.delete = function(x) {
    var key;
    key = _$rapyd$_set_keyfor(x);
    if (Object.hasOwnProperty.call(this._store, key)) {
        this.size -= 1;
        delete this._store[key];
        return true;
    }
    return false;
};
_$rapyd$_dict_polyfill.prototype.has = function(x) {
    return Object.hasOwnProperty.call(this._store, _$rapyd$_set_keyfor(x));
};
_$rapyd$_dict_polyfill.prototype.get = function(x) {
    try {
        return this._store[_$rapyd$_set_keyfor(x)][1];
    } catch (_$rapyd$_Exception) {
        if (_$rapyd$_Exception instanceof TypeError) {
            return undefined;
        } else {
            throw _$rapyd$_Exception;
        }
    }
};
_$rapyd$_dict_polyfill.prototype.values = function(x) {
    var keys, s;
    keys = Object.keys(this._store);
    s = this._store;
    return (function(){
        var _$rapyd$_d = {};
        _$rapyd$_d["_keys"] = keys;
        _$rapyd$_d["_i"] = -1;
        _$rapyd$_d["_s"] = s;
        _$rapyd$_d[_$rapyd$_iterator_symbol] = function() {
            return this;
        };
        _$rapyd$_d["next"] = function() {
            this._i += 1;
            if (this._i >= this._keys.length) {
                return {
                    "done": true
                };
            }
            return {
                "done": false,
                "value": s[this._keys[this._i]][1]
            };
        };
        return _$rapyd$_d;
    })();
};
_$rapyd$_dict_polyfill.prototype.keys = function(x) {
    var keys, s;
    keys = Object.keys(this._store);
    s = this._store;
    return (function(){
        var _$rapyd$_d = {};
        _$rapyd$_d["_keys"] = keys;
        _$rapyd$_d["_i"] = -1;
        _$rapyd$_d["_s"] = s;
        _$rapyd$_d[_$rapyd$_iterator_symbol] = function() {
            return this;
        };
        _$rapyd$_d["next"] = function() {
            this._i += 1;
            if (this._i >= this._keys.length) {
                return {
                    "done": true
                };
            }
            return {
                "done": false,
                "value": s[this._keys[this._i]][0]
            };
        };
        return _$rapyd$_d;
    })();
};
_$rapyd$_dict_polyfill.prototype.entries = function(x) {
    var keys, s;
    keys = Object.keys(this._store);
    s = this._store;
    return (function(){
        var _$rapyd$_d = {};
        _$rapyd$_d["_keys"] = keys;
        _$rapyd$_d["_i"] = -1;
        _$rapyd$_d["_s"] = s;
        _$rapyd$_d[_$rapyd$_iterator_symbol] = function() {
            return this;
        };
        _$rapyd$_d["next"] = function() {
            this._i += 1;
            if (this._i >= this._keys.length) {
                return {
                    "done": true
                };
            }
            return {
                "done": false,
                "value": s[this._keys[this._i]]
            };
        };
        return _$rapyd$_d;
    })();
};
if (typeof Map !== "function" || typeof Map.prototype.delete !== "function") {
    _$rapyd$_dict_implementation = _$rapyd$_dict_polyfill;
} else {
    _$rapyd$_dict_implementation = Map;
}
function _$rapyd$_dict(iterable) {
    if (this instanceof _$rapyd$_dict) {
        this.jsmap = new _$rapyd$_dict_implementation();
        if (iterable !== undefined) {
            this.update(iterable);
        }
        return this;
    } else {
        return new _$rapyd$_dict(iterable);
    }
}
_$rapyd$_dict.prototype.__name__ = "dict";
Object.defineProperties(_$rapyd$_dict.prototype, {
    "length": {
        "get": function() {
            return this.jsmap.size;
        }
    },
    "size": {
        "get": function() {
            return this.jsmap.size;
        }
    }
});
_$rapyd$_dict.prototype.__len__ = function() {
    return this.jsmap.size;
};
_$rapyd$_dict.prototype.has = _$rapyd$_dict.prototype.__contains__ = function(x) {
    return this.jsmap.has(x);
};
_$rapyd$_dict.prototype.set = _$rapyd$_dict.prototype.__setitem__ = function(key, value) {
    this.jsmap.set(key, value);
};
_$rapyd$_dict.prototype.clear = function() {
    this.jsmap.clear();
};
_$rapyd$_dict.prototype.copy = function() {
    return _$rapyd$_dict(this);
};
_$rapyd$_dict.prototype.keys = function() {
    return this.jsmap.keys();
};
_$rapyd$_dict.prototype.values = function() {
    return this.jsmap.values();
};
_$rapyd$_dict.prototype.items = _$rapyd$_dict.prototype.entries = function() {
    return this.jsmap.entries();
};
_$rapyd$_dict.prototype[_$rapyd$_iterator_symbol] = function() {
    return this.jsmap.keys();
};
_$rapyd$_dict.prototype.__getitem__ = function(key) {
    var ans;
    ans = this.jsmap.get(key);
    if (ans === undefined && !this.jsmap.has(key)) {
        throw new KeyError(key + "");
    }
    return ans;
};
_$rapyd$_dict.prototype.get = function(key, defval) {
    var ans;
    ans = this.jsmap.get(key);
    if (ans === undefined && !this.jsmap.has(key)) {
        return (defval === undefined) ? null : defval;
    }
    return ans;
};
_$rapyd$_dict.prototype.set_default = function(key, defval) {
    var j;
    j = this.jsmap;
    if (!j.has(key)) {
        j.set(key, defval);
        return defval;
    }
    return j.get(key);
};
_$rapyd$_dict.fromkeys = _$rapyd$_dict.prototype.fromkeys = function() {
    var iterable = ( 0 === arguments.length-1 && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [_$rapyd$_kwargs_symbol] === true) ? undefined : arguments[0];
    var value = (arguments[1] === undefined || ( 1 === arguments.length-1 && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [_$rapyd$_kwargs_symbol] === true)) ? (null) : arguments[1];
    var _$rapyd$_kwargs_obj = arguments[arguments.length-1];
    if (typeof _$rapyd$_kwargs_obj !== "object" || _$rapyd$_kwargs_obj [_$rapyd$_kwargs_symbol] !== true) _$rapyd$_kwargs_obj = {};
    if (Object.prototype.hasOwnProperty.call(_$rapyd$_kwargs_obj, "value")){
        value = _$rapyd$_kwargs_obj.value;
    }
    var ans, iterator, r;
    ans = _$rapyd$_dict();
    iterator = iter(iterable);
    r = iterator.next();
    while (!r.done) {
        ans.set(r.value, value);
        r = iterator.next();
    }
    return ans;
};
_$rapyd$_dict.prototype.pop = function(key, defval) {
    var ans;
    ans = this.jsmap.get(key);
    if (ans === undefined && !this.jsmap.has(key)) {
        if (defval === undefined) {
            throw new KeyError(key);
        }
        return defval;
    }
    this.jsmap.delete(key);
    return ans;
};
_$rapyd$_dict.prototype.popitem = function() {
    var r;
    r = this.jsmap.entries().next();
    if (r.done) {
        throw new KeyError("dict is empty");
    }
    this.jsmap.delete(r.value[0]);
    return r.value;
};
_$rapyd$_dict.prototype.update = function() {
    var m, iterable, iterator, result, keys;
    if (arguments.length === 0) {
        return;
    }
    m = this.jsmap;
    iterable = arguments[0];
    if (Array.isArray(iterable)) {
        for (var i = 0; i < iterable.length; i++) {
            m.set(iterable[i][0], iterable[i][1]);
        }
    } else if (iterable instanceof _$rapyd$_dict) {
        iterator = iterable.items();
        result = iterator.next();
        while (!result.done) {
            m.set(result.value[0], result.value[1]);
            result = iterator.next();
        }
    } else if (typeof Map === "function" && iterable instanceof Map) {
        iterator = iterable.entries();
        result = iterator.next();
        while (!result.done) {
            m.set(result.value[0], result.value[1]);
            result = iterator.next();
        }
    } else if (typeof iterable[_$rapyd$_iterator_symbol] === "function") {
        iterator = iterable[_$rapyd$_iterator_symbol]();
        result = iterator.next();
        while (!result.done) {
            m.set(result.value[0], result.value[1]);
            result = iterator.next();
        }
    } else {
        keys = Object.keys(iterable);
        for (var i=0; i < keys.length; i++) {
            if (keys[i] !== _$rapyd$_iterator_symbol) {
                m.set(keys[i], iterable[keys[i]]);
            }
        }
    }
    if (arguments.length > 1) {
        _$rapyd$_dict.prototype.update.call(this, arguments[1]);
    }
};
_$rapyd$_dict.prototype.toString = _$rapyd$_dict.prototype.inspect = function() {
    var entries, iterator, r;
    entries = [];
    iterator = this.jsmap.entries();
    r = iterator.next();
    while (!r.done) {
        entries.push(r.value[0] + ": " + r.value[1]);
        r = iterator.next();
    }
    return "{" + entries.join(", ") + "}";
};
_$rapyd$_dict.prototype.__eq__ = function(other) {
    var iterator, r, x;
    if (!(other instanceof this.constructor)) {
        return false;
    }
    if (other.size !== this.size) {
        return false;
    }
    if (other.size === 0) {
        return true;
    }
    iterator = other.items();
    r = iterator.next();
    while (!r.done) {
        x = this.jsmap.get(r.value[0]);
        if (x === undefined && !this.jsmap.has(r.value[0]) || x !== r.value[1]) {
            return false;
        }
        r = iterator.next();
    }
    return true;
};
_$rapyd$_dict.prototype.as_object = function(other) {
    var ans, iterator, r;
    ans = {};
    iterator = this.jsmap.entries();
    r = iterator.next();
    while (!r.done) {
        ans[r.value[0]] = r.value[1];
        r = iterator.next();
    }
    return ans;
};
function _$rapyd$_dict_wrap(x) {
    var ans;
    ans = new _$rapyd$_dict();
    ans.jsmap = x;
    return ans;
}
var dict = _$rapyd$_dict, dict_wrap = _$rapyd$_dict_wrap;
    function _$rapyd$_bool(val) {
    return !!val;
}
function _$rapyd$_bind(fn, thisArg) {
    var ret;
    if (fn.orig) {
        fn = fn.orig;
    }
    if (thisArg === false) {
        return fn;
    }
    ret = function() {
        return fn.apply(thisArg, arguments);
    };
    ret.orig = fn;
    return ret;
}
function _$rapyd$_rebind_all(thisArg, rebind) {
    if (typeof rebind === "undefined") {
        rebind = true;
    }
    for (var p in thisArg) {
        if (thisArg[p] && thisArg[p].orig) {
            if (rebind) {
                thisArg[p] = _$rapyd$_bind(thisArg[p], thisArg);
            } else {
                thisArg[p] = thisArg[p].orig;
            }
        }
    }
}
function _$rapyd$_eslice(arr, step, start, end) {
    var isString;
    arr = arr.slice(0);
    if (typeof arr === "string" || arr instanceof String) {
        isString = true;
        arr = arr.split("");
    }
    if (step < 0) {
        step = -step;
        arr.reverse();
        if (typeof start !== "undefined") {
            start = arr.length - start - 1;
        }
        if (typeof end !== "undefined") {
            end = arr.length - end - 1;
        }
    }
    if (typeof start === "undefined") {
        start = 0;
    }
    if (typeof end === "undefined") {
        end = arr.length;
    }
    arr = arr.slice(start, end).filter(function(e, i) {
        return i % step === 0;
    });
    return (isString) ? arr.join("") : arr;
}
function _$rapyd$_mixin(target, source, overwrite) {
    for (var i in source) {
        if (source.hasOwnProperty(i) && overwrite || typeof target[i] === "undefined") {
            target[i] = source[i];
        }
    }
}
function _$rapyd$_print() {
    var parts, part;
    if (typeof console === "object") {
        parts = [];
        for (i = 0; i < arguments.length; i++) {
            part = arguments[i];
            if (typeof part === "string") {
                parts.push(part);
            } else if (part === null) {
                parts.push("None");
            } else if (typeof part === "boolean") {
                parts.push((part) ? "True" : "False");
            } else {
                try {
                    parts.push(JSON.stringify(part));
                } catch (_$rapyd$_Exception) {
                    parts.push(part.toString());
                }
            }
        }
        console.log(parts.join(" "));
    }
}
function _$rapyd$_int(val, base) {
    var ans;
    ans = parseInt(val, base || 10);
    if (isNaN(ans)) {
        throw new ValueError("Invalid literal for int with base " + (base || 10) + ": " + val);
    }
    return ans;
}
function _$rapyd$_float() {
    var ans;
    ans = parseFloat.apply(null, arguments);
    if (isNaN(ans)) {
        throw new ValueError("Could not convert string to float: " + arguments[0]);
    }
    return ans;
}
function options_object(f) {
    return function() {
        if (typeof arguments[arguments.length - 1] === "object") {
            arguments[arguments.length - 1][_$rapyd$_kwargs_symbol] = true;
        }
        return f.apply(this, arguments);
    };
}
var bool = _$rapyd$_bool, bind = _$rapyd$_bind, rebind_all = _$rapyd$_rebind_all;
var float = _$rapyd$_float, int = _$rapyd$_int, rebind_all = _$rapyd$_rebind_all;
var mixin = _$rapyd$_mixin, print = _$rapyd$_print, eslice = _$rapyd$_eslice;
    function _$rapyd$_str() {
    return arguments[0] + "";
}
_$rapyd$_str.format = function() {
    var template, args, kwargs, explicit, implicit, idx, ans, pos, in_brace, markup, ch;
    template = arguments[0];
    if (template === undefined) {
        throw TypeError("Template is required");
    }
    args = Array.prototype.slice.call(arguments, 1);
    kwargs = {};
    if (args.length && args[args.length-1][_$rapyd$_kwargs_symbol] !== undefined) {
        kwargs = args[args.length-1];
        args = args.slice(0, -1);
    }
    explicit = implicit = false;
    idx = 0;
    if (_$rapyd$_str.format._template_resolve_pat === undefined) {
        _$rapyd$_str.format._template_resolve_pat = /[.\[]/;
    }
    function resolve(arg, object) {
        var _$rapyd$_Unpack, first, key, rest, ans;
        if (!arg) {
            return object;
        }
        _$rapyd$_Unpack = [arg[0], arg.slice(1)];
        first = _$rapyd$_Unpack[0];
        arg = _$rapyd$_Unpack[1];
        key = arg.split(_$rapyd$_str.format._template_resolve_pat, 1)[0];
        rest = arg.slice(key.length);
        ans = (first === "[") ? object[key.slice(0, -1)] : getattr(object, key);
        if (ans === undefined) {
            throw new KeyError((first === "[") ? key.slice(0, -1) : key);
        }
        return resolve(rest, ans);
    }
    function resolve_format_spec(format_spec) {
        if (_$rapyd$_str.format._template_resolve_fs_pat === undefined) {
            _$rapyd$_str.format._template_resolve_fs_pat = /[{]([a-zA-Z0-9_]+)[}]/g;
        }
        return format_spec.replace(_$rapyd$_str.format._template_resolve_fs_pat, function(match, key) {
            if (!Object.prototype.hasOwnProperty.call(kwargs, key)) {
                return "";
            }
            return "" + kwargs[key];
        });
    }
    function apply_formatting(value, format_spec) {
        var _$rapyd$_Unpack, fill, align, sign, fhash, zeropad, width, comma, precision, ftype, is_numeric, is_int, lftype, code, exp, nval, is_positive, left, right;
        if (format_spec.indexOf("{") !== -1) {
            format_spec = resolve_format_spec(format_spec);
        }
        if (_$rapyd$_str.format._template_format_pat === undefined) {
            _$rapyd$_str.format._template_format_pat = /([^{}](?=[<>=^]))?([<>=^])?([-+\x20])?(\#)?(0)?(\d+)?(,)?(?:\.(\d+))?([bcdeEfFgGnosxX%])?/;
        }
        try {
            _$rapyd$_Unpack = format_spec.match(_$rapyd$_str.format._template_format_pat).slice(1);
            fill = _$rapyd$_Unpack[0];
            align = _$rapyd$_Unpack[1];
            sign = _$rapyd$_Unpack[2];
            fhash = _$rapyd$_Unpack[3];
            zeropad = _$rapyd$_Unpack[4];
            width = _$rapyd$_Unpack[5];
            comma = _$rapyd$_Unpack[6];
            precision = _$rapyd$_Unpack[7];
            ftype = _$rapyd$_Unpack[8];
        } catch (_$rapyd$_Exception) {
            if (_$rapyd$_Exception instanceof TypeError) {
                return value;
            } else {
                throw _$rapyd$_Exception;
            }
        }
        if (zeropad) {
            fill = fill || "0";
            align = align || "=";
        } else {
            fill = fill || " ";
            align = align || ">";
        }
        is_numeric = Number(value) === value;
        is_int = is_numeric && value % 1 === 0;
        precision = parseInt(precision, 10);
        lftype = (ftype || "").toLowerCase();
        if (ftype === "n") {
            is_numeric = true;
            if (is_int) {
                if (comma) {
                    throw new ValueError("Cannot specify ',' with 'n'");
                }
                value = parseInt(value, 10).toLocaleString();
            } else {
                value = parseFloat(value).toLocaleString();
            }
        } else if (['b', 'c', 'd', 'o', 'x'].indexOf(lftype) !== -1) {
            value = parseInt(value, 10);
            is_numeric = true;
            if (!isNaN(value)) {
                if (ftype === "b") {
                    value = (value >>> 0).toString(2);
                    if (fhash) {
                        value = "0b" + value;
                    }
                } else if (ftype === "c") {
                    if (value > 65535) {
                        code = value - 65536;
                        value = String.fromCharCode(55296 + (code >> 10), 56320 + (code & 1023));
                    } else {
                        value = String.fromCharCode(value);
                    }
                } else if (ftype === "d") {
                    if (comma) {
                        value = value.toLocaleString("en-US");
                    } else {
                        value = value.toString(10);
                    }
                } else if (ftype === "o") {
                    value = value.toString(8);
                    if (fhash) {
                        value = "0o" + value;
                    }
                } else if (lftype === "x") {
                    value = value.toString(16);
                    value = (ftype === "x") ? value.toLowerCase() : value.toUpperCase();
                    if (fhash) {
                        value = "0x" + value;
                    }
                }
            }
        } else if (['e','f','g','%'].indexOf(lftype) !== -1) {
            is_numeric = true;
            value = parseFloat(value);
            if (lftype === "e") {
                value = value.toExponential((isNaN(precision)) ? 6 : precision);
                value = (ftype === "E") ? value.toUpperCase() : value.toLowerCase();
            } else if (lftype === "f") {
                value = value.toFixed((isNaN(precision)) ? 6 : precision);
                value = (ftype === "F") ? value.toUpperCase() : value.toLowerCase();
            } else if (ftype === "%") {
                value *= 100;
                value = value.toFixed((isNaN(precision)) ? 6 : precision) + "%";
            } else if (lftype === "g") {
                if (isNaN(precision)) {
                    precision = 6;
                }
                precision = max(1, precision);
                exp = parseInt(value.toExponential(precision - 1).toLowerCase().split("e")[1], 10);
                if (-4 <= exp && exp < precision) {
                    value = value.toFixed(precision - 1 - exp);
                } else {
                    value = value.toExponential(precision - 1);
                }
                value = value.replace(/0+$/g, "");
                if (value[value.length-1] === ".") {
                    value = value.slice(0, -1);
                }
                if (ftype === "G") {
                    value = value.toUpperCase();
                }
            }
        } else {
            value += "";
            if (!isNaN(precision)) {
                value = value.slice(0, precision);
            }
        }
        value += "";
        if (is_numeric && sign) {
            nval = new Number(value);
            is_positive = !isNaN(nval) && nval >= 0;
            if (is_positive && (sign === " " || sign === "+")) {
                value = sign + value;
            }
        }
        function repeat(char, num) {
            return Array(num+1).join(char);
        }
        if (is_numeric && width && width[0] === "0") {
            width = width.slice(1);
            _$rapyd$_Unpack = ["0", "="];
            fill = _$rapyd$_Unpack[0];
            align = _$rapyd$_Unpack[1];
        }
        width = parseInt(width || "-1", 10);
        if (isNaN(width)) {
            throw new ValueError("Invalid width specification: " + width);
        }
        if (fill && value.length < width) {
            if (align === "<") {
                value = value + repeat(fill, width - value.length);
            } else if (align === ">") {
                value = repeat(fill, width - value.length) + value;
            } else if (align === "^") {
                left = Math.floor((width - value.length) / 2);
                right = width - left - value.length;
                value = repeat(fill, left) + value + repeat(fill, right);
            } else if (align === "=") {
                if (_$rapyd$_in(value[0], "+- ")) {
                    value = value[0] + repeat(fill, width - value.length) + value.slice(1);
                } else {
                    value = repeat(fill, width - value.length) + value;
                }
            } else {
                throw new ValueError("Unrecognized alignment: " + align);
            }
        }
        return value;
    }
    function parse_markup(markup) {
        var key, transformer, pos, state, ch, format_spec;
        key = transformer = format_spec = "";
        pos = 0;
        state = 0;
        while (pos < markup.length) {
            ch = markup[pos];
            if (state === 0) {
                if (ch === "!") {
                    state = 1;
                } else if (ch === ":") {
                    state = 2;
                } else {
                    key += ch;
                }
            } else if (state === 1) {
                if (ch === ":") {
                    state = 2;
                } else {
                    transformer += ch;
                }
            } else {
                format_spec += ch;
            }
            pos += 1;
        }
        return [key, transformer, format_spec];
    }
    function render_markup(markup) {
        var _$rapyd$_Unpack, key, transformer, format_spec, lkey, nvalue, object, ans;
        _$rapyd$_Unpack = parse_markup(markup);
        key = _$rapyd$_Unpack[0];
        transformer = _$rapyd$_Unpack[1];
        format_spec = _$rapyd$_Unpack[2];
        if (transformer && ['a', 'r', 's'].indexOf(transformer) === -1) {
            throw new ValueError("Unknown conversion specifier: " + transformer);
        }
        lkey = key.length && key.split(/[.\[]/, 1)[0];
        if (lkey) {
            explicit = true;
            if (implicit) {
                throw new ValueError("cannot switch from automatic field numbering to manual field specification");
            }
            nvalue = parseInt(lkey);
            object = (isNaN(nvalue)) ? kwargs[lkey] : args[nvalue];
            if (object === undefined) {
                if (isNaN(nvalue)) {
                    throw new KeyError(lkey);
                }
                throw new IndexError(lkey);
            }
            object = resolve(key.slice(lkey.length), object);
        } else {
            implicit = true;
            if (explicit) {
                throw new ValueError("cannot switch from manual field specification to automatic field numbering");
            }
            if (idx >= args.length) {
                throw new IndexError("Not enough arguments to match template: " + template);
            }
            object = args[idx];
            idx += 1;
        }
        if (typeof object === "function") {
            object = object();
        }
        ans = "" + object;
        if (format_spec) {
            ans = apply_formatting(ans, format_spec);
        }
        return ans;
    }
    ans = "";
    pos = 0;
    in_brace = 0;
    markup = "";
    while (pos < template.length) {
        ch = template[pos];
        if (in_brace) {
            if (ch === "{") {
                in_brace += 1;
                markup += "{";
            } else if (ch === "}") {
                in_brace -= 1;
                if (in_brace > 0) {
                    markup += "}";
                } else {
                    ans += render_markup(markup);
                }
            } else {
                markup += ch;
            }
        } else {
            if (ch === "{") {
                if (template[pos + 1] === "{") {
                    pos += 1;
                    ans += "{";
                } else {
                    in_brace = 1;
                    markup = "";
                }
            } else {
                ans += ch;
            }
        }
        pos += 1;
    }
    if (in_brace) {
        throw new ValueError("expected '}' before end of string");
    }
    return ans;
};
_$rapyd$_str.capitalize = function(string) {
    if (string) {
        string = string[0].toUpperCase() + string.slice(1).toLowerCase();
    }
    return string;
};
_$rapyd$_str.center = function(string, width, fill) {
    var left, right;
    left = Math.floor((width - string.length) / 2);
    right = width - left - string.length;
    fill = fill || " ";
    return Array(left+1).join(fill) + string + Array(right+1).join(fill);
};
_$rapyd$_str.count = function(string, needle, start, end) {
    var _$rapyd$_Unpack, pos, step, ans;
    start = start || 0;
    end = end || string.length;
    if (start < 0 || end < 0) {
        string = string.slice(start, end);
        _$rapyd$_Unpack = [0, string.length];
        start = _$rapyd$_Unpack[0];
        end = _$rapyd$_Unpack[1];
    }
    pos = start;
    step = needle.length;
    ans = 0;
    while (pos !== -1) {
        pos = string.indexOf(needle, pos);
        if (pos !== -1) {
            ans += 1;
            pos += step;
        }
    }
    return ans;
};
_$rapyd$_str.endswith = function(string, suffixes, start, end) {
    var q;
    start = start || 0;
    if (typeof suffixes === "string") {
        suffixes = [suffixes];
    }
    if (end !== undefined) {
        string = string.slice(0, end);
    }
    for (var i = 0; i < suffixes.length; i++) {
        q = suffixes[i];
        if (string.indexOf(q, Math.max(start, string.length - q.length)) !== -1) {
            return true;
        }
    }
    return false;
};
_$rapyd$_str.startswith = function(string, prefixes, start, end) {
    var prefix;
    start = start || 0;
    if (typeof prefixes === "string") {
        prefixes = [prefixes];
    }
    for (var i = 0; i < prefixes.length; i++) {
        prefix = prefixes[i];
        end = (end === undefined) ? string.length : end;
        if (end - start >= prefix.length && prefix === string.slice(start, start + prefix.length)) {
            return true;
        }
    }
    return false;
};
_$rapyd$_str.find = function(string, needle, start, end) {
    var ans;
    while (start < 0) {
        start += string.length;
    }
    ans = string.indexOf(needle, start);
    if (end !== undefined && ans !== -1) {
        while (end < 0) {
            end += string.length;
        }
        if (ans >= end - needle.length) {
            return -1;
        }
    }
    return ans;
};
_$rapyd$_str.rfind = function(string, needle, start, end) {
    var ans;
    while (end < 0) {
        end += string.length;
    }
    ans = string.lastIndexOf(needle, end - 1);
    if (start !== undefined && ans !== -1) {
        while (start < 0) {
            start += string.length;
        }
        if (ans < start) {
            return -1;
        }
    }
    return ans;
};
_$rapyd$_str.index = function(string, needle, start, end) {
    var ans;
    ans = _$rapyd$_str.find.apply(null, arguments);
    if (ans === -1) {
        throw new ValueError("substring not found");
    }
    return ans;
};
_$rapyd$_str.rindex = function(string, needle, start, end) {
    var ans;
    ans = _$rapyd$_str.rfind.apply(null, arguments);
    if (ans === -1) {
        throw new ValueError("substring not found");
    }
    return ans;
};
_$rapyd$_str.islower = function(string) {
    return string.length > 0 && string.toUpperCase() !== string;
};
_$rapyd$_str.isupper = function(string) {
    return string.length > 0 && string.toLowerCase() !== string;
};
_$rapyd$_str.isspace = function(string) {
    return string.length > 0 && /^\s+$/.test(string);
};
_$rapyd$_str.join = function(string, iterable) {
    var ans, r;
    if (Array.isArray(iterable)) {
        return iterable.join(string);
    }
    ans = "";
    r = iterable.next();
    while (!r.done) {
        if (ans) {
            ans += string;
        }
        ans += r.value;
        r = iterable.next();
    }
    return ans;
};
_$rapyd$_str.ljust = function(string, width, fill) {
    if (width > string.length) {
        fill = fill || " ";
        string += Array(width - string.length + 1).join(fill);
    }
    return string;
};
_$rapyd$_str.rjust = function(string, width, fill) {
    if (width > string.length) {
        fill = fill || " ";
        string = Array(width - string.length + 1).join(fill) + string;
    }
    return string;
};
_$rapyd$_str.lower = function(string) {
    return string.toLowerCase();
};
_$rapyd$_str.upper = function(string) {
    return string.toUpperCase();
};
_$rapyd$_str.lstrip = function(string, chars) {
    var pos;
    pos = 0;
    chars = chars || _$rapyd$_str.whitespace;
    while (chars.indexOf(string[pos]) !== -1) {
        pos += 1;
    }
    if (pos) {
        string = string.slice(pos);
    }
    return string;
};
_$rapyd$_str.rstrip = function(string, chars) {
    var pos;
    pos = string.length - 1;
    chars = chars || _$rapyd$_str.whitespace;
    while (chars.indexOf(string[pos]) !== -1) {
        pos -= 1;
    }
    if (pos < string.length - 1) {
        string = string.slice(0, pos + 1);
    }
    return string;
};
_$rapyd$_str.strip = function(string, chars) {
    return _$rapyd$_str.lstrip(_$rapyd$_str.rstrip(string, chars), chars);
};
_$rapyd$_str.partition = function(string, sep) {
    var idx;
    idx = string.indexOf(sep);
    if (idx === -1) {
        return [string, "", ""];
    }
    return [string.slice(0, idx), sep, string.slice(idx + sep.length)];
};
_$rapyd$_str.rpartition = function(string, sep) {
    var idx;
    idx = string.lastIndexOf(sep);
    if (idx === -1) {
        return ["", "", string];
    }
    return [string.slice(0, idx), sep, string.slice(idx + sep.length)];
};
_$rapyd$_str.replace = function(string, old, repl, count) {
    var pos, idx;
    if (count === 1) {
        return string.replace(old, repl);
    }
    if (count < 1) {
        return string;
    }
    count = count || Number.MAX_VALUE;
    pos = 0;
    while (count > 0) {
        count -= 1;
        idx = string.indexOf(old, pos);
        if (idx === -1) {
            break;
        }
        pos = idx + repl.length;
        string = string.slice(0, idx) + repl + string.slice(idx + old.length);
    }
    return string;
};
_$rapyd$_str.split = function(string, sep, maxsplit) {
    var ans, extra, parts;
    if (maxsplit === 0) {
        return _$rapyd$_list_decorate([ string ]);
    }
    if (sep === undefined || sep === null) {
        if (maxsplit > 0) {
            ans = string.split(/(\s+)/);
            extra = "";
            parts = [];
            for (var i = 0; i < ans.length; i++) {
                if (parts.length >= maxsplit + 1) {
                    extra += ans[i];
                } else if (i % 2 === 0) {
                    parts.push(ans[i]);
                }
            }
            parts[parts.length-1] += extra;
            ans = parts;
        } else {
            ans = string.split(/\s+/);
        }
    } else {
        if (sep === "") {
            throw new ValueError("empty separator");
        }
        ans = string.split(sep);
        if (maxsplit > 0 && ans.length > maxsplit) {
            extra = ans.slice(maxsplit).join(sep);
            ans = ans.slice(0, maxsplit);
            ans.push(extra);
        }
    }
    return _$rapyd$_list_decorate(ans);
};
_$rapyd$_str.rsplit = function(string, sep, maxsplit) {
    var ans, is_space, pos, current, spc, ch, end, idx;
    if (!maxsplit) {
        return _$rapyd$_str.split.call(null, string, sep, maxsplit);
    }
    if (sep === undefined || sep === null) {
        if (maxsplit > 0) {
            ans = [];
            is_space = /\s/;
            pos = string.length - 1;
            current = "";
            while (pos > -1 && maxsplit > 0) {
                spc = false;
                ch = string[pos];
                while (pos > -1 && is_space.test(ch)) {
                    spc = true;
                    ch = string[--pos];
                }
                if (spc) {
                    if (current) {
                        ans.push(current);
                        maxsplit -= 1;
                    }
                    current = ch;
                } else {
                    current += ch;
                }
                pos -= 1;
            }
            ans.push(string.slice(0, pos + 1) + current);
            ans.reverse();
        } else {
            ans = string.split(/\s+/);
        }
    } else {
        if (sep === "") {
            throw new ValueError("empty separator");
        }
        ans = [];
        pos = end = string.length;
        while (pos > -1 && maxsplit > 0) {
            maxsplit -= 1;
            idx = string.lastIndexOf(sep, pos);
            if (idx === -1) {
                break;
            }
            ans.push(string.slice(idx + sep.length, end));
            pos = idx - 1;
            end = idx;
        }
        ans.push(string.slice(0, end));
        ans.reverse();
    }
    return _$rapyd$_list_decorate(ans);
};
_$rapyd$_str.splitlines = function(string, keepends) {
    var parts, ans;
    if (keepends) {
        parts = string.split(/((?:\r?\n)|\r)/);
        ans = [];
        for (var i = 0; i < parts.length; i++) {
            if (i % 2 === 0) {
                ans.push(parts[i]);
            } else {
                ans[ans.length-1] += parts[i];
            }
        }
    } else {
        ans = string.split(/(?:\r?\n)|\r/);
    }
    return _$rapyd$_list_decorate(ans);
};
_$rapyd$_str.swapcase = function(string) {
    var ans, a, b;
    ans = Array(string.length);
    for (var i = 0; i < ans.length; i++) {
        a = string[i];
        b = a.toLowerCase();
        if (a === b) {
            b = a.toUpperCase();
        }
        ans[i] = b;
    }
    return ans.join("");
};
_$rapyd$_str.zfill = function(string, width) {
    if (width > string.length) {
        string = Array(width - string.length + 1).join("0") + string;
    }
    return string;
};
_$rapyd$_str.uchrs = function(string, with_positions) {
    return (function(){
        var _$rapyd$_d = {};
        _$rapyd$_d["_string"] = string;
        _$rapyd$_d["_pos"] = 0;
        _$rapyd$_d[_$rapyd$_iterator_symbol] = function() {
            return this;
        };
        _$rapyd$_d["next"] = function() {
            var length, pos, value, ans, extra;
            length = this._string.length;
            if (this._pos >= length) {
                return {
                    "done": true
                };
            }
            pos = this._pos;
            value = this._string.charCodeAt(this._pos++);
            ans = "\ufffd";
            if (55296 <= value && value <= 56319) {
                if (this._pos < length) {
                    extra = this._string.charCodeAt(this._pos++);
                    if ((extra & 56320) === 56320) {
                        ans = String.fromCharCode(value, extra);
                    }
                }
            } else if ((value & 56320) !== 56320) {
                ans = String.fromCharCode(value);
            }
            if (with_positions) {
                return {
                    "done": false,
                    "value": _$rapyd$_list_decorate([ pos, ans ])
                };
            } else {
                return {
                    "done": false,
                    "value": ans
                };
            }
        };
        return _$rapyd$_d;
    })();
};
_$rapyd$_str.uslice = function(string, start, end) {
    var items, iterator, r;
    items = [];
    iterator = _$rapyd$_str.uchrs(string);
    r = iterator.next();
    while (!r.done) {
        items.push(r.value);
        r = iterator.next();
    }
    return items.slice(start || 0, (end === undefined) ? items.length : end).join("");
};
_$rapyd$_str.ulen = function(string) {
    var iterator, r, ans;
    iterator = _$rapyd$_str.uchrs(string);
    r = iterator.next();
    ans = 0;
    while (!r.done) {
        r = iterator.next();
        ans += 1;
    }
    return ans;
};
_$rapyd$_str.ascii_lowercase = "abcdefghijklmnopqrstuvwxyz";
_$rapyd$_str.ascii_uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
_$rapyd$_str.ascii_letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
_$rapyd$_str.digits = "0123456789";
_$rapyd$_str.punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";
_$rapyd$_str.printable = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\u000b\f";
_$rapyd$_str.whitespace = " \t\n\r\u000b\f";
var str = _$rapyd$_str;
    function _$rapyd$_extends(child, parent) {
            child.prototype = Object.create(parent.prototype);
            child.prototype.constructor = child;
        }
    var min = (function min() {
            return Math.min;
        })();
    var max = (function max() {
            return Math.max;
        })();
    function iter(iterable) {
            var ans;
            if (typeof iterable[_$rapyd$_iterator_symbol] === "function") {
                return (typeof Map === "function" && iterable instanceof Map) ? iterable.keys() : iterable[_$rapyd$_iterator_symbol]();
            }
            if (Array.isArray(iterable) || typeof iterable === "string") {
                ans = {
                    "_i": -1,
                    "next": function() {
                        this._i += 1;
                        if (this._i < iterable.length) {
                            return {
                                "done": false,
                                "value": iterable[this._i]
                            };
                        }
                        return {
                            "done": true
                        };
                    }
                };
                ans[_$rapyd$_iterator_symbol] = function() {
                    return this;
                };
                return ans;
            }
            return iter(Object.keys(iterable));
        }
    function getattr(obj, name, defval) {
            var ret;
            try {
                ret = obj[name];
            } catch (_$rapyd$_Exception) {
                if (_$rapyd$_Exception instanceof TypeError) {
                    if (defval === undefined) {
                        throw new AttributeError("The attribute " + name + " is not present");
                    }
                    return defval;
                } else {
                    throw _$rapyd$_Exception;
                }
            }
            if (ret === undefined && !(name in obj)) {
                if (defval === undefined) {
                    throw new AttributeError("The attribute " + name + " is not present");
                }
                ret = defval;
            }
            return ret;
        }
    var _$rapyd$_modules = {};
    _$rapyd$_modules["qt"] = {};
    _$rapyd$_modules["middle_click"] = {};
    _$rapyd$_modules["focus"] = {};
    _$rapyd$_modules["elementmaker"] = {};
    _$rapyd$_modules["humanize"] = {};
    _$rapyd$_modules["downloads"] = {};

    (function(){
        var __name__ = "qt";
        var bridge, channel, bridge_name;
        bridge = null;
        channel = null;
        bridge_name = "ͻ-qt-js-bridge";
        function qt_bridge() {
            if (window.self !== window.top) {
                return window.top[bridge_name];
            }
            return bridge;
        }
        function callback(name, data, console_err) {
            var bridge;
            bridge = qt_bridge();
            if (bridge === null) {
                console.error(console_err || "Aborting callback: " + name + " as Qt bridge not available");
            } else {
                bridge.callback(name, JSON.stringify(data));
            }
        }
        function connect_bridge(proceed) {
            if (window.self !== window.top) {
                proceed();
                return;
            }
            channel = new QWebChannel(qt.webChannelTransport, function(channel) {
                bridge = channel.objects.bridge;
                Object.defineProperty(window, bridge_name, {
                    "value": bridge
                });
                proceed();
            });
        }
        _$rapyd$_modules["qt"]["bridge"] = bridge;

        _$rapyd$_modules["qt"]["channel"] = channel;

        _$rapyd$_modules["qt"]["bridge_name"] = bridge_name;

        _$rapyd$_modules["qt"]["qt_bridge"] = qt_bridge;

        _$rapyd$_modules["qt"]["callback"] = callback;

        _$rapyd$_modules["qt"]["connect_bridge"] = connect_bridge;
    })();

    (function(){
        var __name__ = "middle_click";
        var qt_bridge = _$rapyd$_modules["qt"].qt_bridge;
        
        function find_link(node) {
            if (node && node.nodeType === Node.ELEMENT_NODE) {
                if (node.nodeName.toUpperCase() === "A" && node.getAttribute("href")) {
                    return node.href;
                }
                return find_link(node.parentElement);
            }
        }
        function handle_middle_click(ev) {
            var href, bridge;
            if (ev.button !== 1) {
                return true;
            }
            href = find_link(ev.target);
            if (!href) {
                return true;
            }
            bridge = qt_bridge();
            if (!bridge) {
                console.error("The JS-to-python bridge is not initialized, ignoring middle click");
                return true;
            }
            bridge.middle_clicked_link(href);
            ev.preventDefault();
            ev.stopPropagation();
            return false;
        }
        function onload() {
            document.addEventListener("click", handle_middle_click);
        }
        _$rapyd$_modules["middle_click"]["find_link"] = find_link;

        _$rapyd$_modules["middle_click"]["handle_middle_click"] = handle_middle_click;

        _$rapyd$_modules["middle_click"]["onload"] = onload;
    })();

    (function(){
        var __name__ = "focus";
        var edit_counter;
        var qt_bridge = _$rapyd$_modules["qt"].qt_bridge;
        
        function text_editing_allowed(node) {
            return !node.hasAttribute("readonly") && !node.hasAttribute("disabled");
        }
        function is_text_input_node(node) {
            var name, itype;
            if (node && node.nodeType === Node.ELEMENT_NODE) {
                name = node.nodeName.toUpperCase();
                if (name === "TEXTAREA") {
                    return text_editing_allowed(node);
                }
                if (name === "INPUT") {
                    itype = (node.getAttribute("type") || "").toLowerCase();
                    if (!(_$rapyd$_in(itype, (function(){
                        var s = _$rapyd$_set();
                        s.jsset.add("hidden");
                        s.jsset.add("image");
                        s.jsset.add("button");
                        s.jsset.add("reset");
                        s.jsset.add("file");
                        s.jsset.add("reset");
                        s.jsset.add("radio");
                        s.jsset.add("submit");
                        return s;
                    })()))) {
                        return text_editing_allowed(node);
                    }
                }
            }
            return false;
        }
        function get_bridge() {
            var msg = (arguments[0] === undefined || ( 0 === arguments.length-1 && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [_$rapyd$_kwargs_symbol] === true)) ? ("ignoring focus event") : arguments[0];
            var _$rapyd$_kwargs_obj = arguments[arguments.length-1];
            if (typeof _$rapyd$_kwargs_obj !== "object" || _$rapyd$_kwargs_obj [_$rapyd$_kwargs_symbol] !== true) _$rapyd$_kwargs_obj = {};
            if (Object.prototype.hasOwnProperty.call(_$rapyd$_kwargs_obj, "msg")){
                msg = _$rapyd$_kwargs_obj.msg;
            }
            var bridge;
            bridge = qt_bridge();
            if (!bridge) {
                console.error("The JS-to-python bridge is not initialized, " + msg);
            }
            return bridge;
        }
        function handle_focus_in(ev) {
            var bridge;
            bridge = get_bridge();
            if (bridge) {
                bridge.element_focused(is_text_input_node(document.activeElement));
            }
            return true;
        }
        function handle_focus_out(ev) {
            var bridge;
            bridge = get_bridge();
            if (bridge) {
                bridge.element_focused(false);
            }
            return true;
        }
        edit_counter = 0;
        function get_editable_text() {
            var bridge, elem, text;
            bridge = get_bridge("ignoring get_editable_text()");
            if (!bridge) {
                return;
            }
            elem = document.activeElement;
            if (text_editing_allowed(elem)) {
                text = elem.value;
                edit_counter += 1;
                elem.setAttribute("data-vise-edit-text", edit_counter + "");
                bridge.edit_text(text || "", edit_counter + "");
            }
        }
        function set_editable_text(text, eid) {
            var elem;
            elem = document.querySelector("[data-vise-edit-text=\"" + eid + "\"]");
            if (elem) {
                elem.value = text;
            }
        }
        function onload() {
            document.addEventListener("focusin", handle_focus_in, true);
            document.addEventListener("focusout", handle_focus_out, true);
            if (window.vise_get_editable_text === undefined) {
                Object.defineProperty(window, "vise_get_editable_text", {
                    "value": get_editable_text
                });
                Object.defineProperty(window, "vise_set_editable_text", {
                    "value": set_editable_text
                });
            }
        }
        _$rapyd$_modules["focus"]["edit_counter"] = edit_counter;

        _$rapyd$_modules["focus"]["text_editing_allowed"] = text_editing_allowed;

        _$rapyd$_modules["focus"]["is_text_input_node"] = is_text_input_node;

        _$rapyd$_modules["focus"]["get_bridge"] = get_bridge;

        _$rapyd$_modules["focus"]["handle_focus_in"] = handle_focus_in;

        _$rapyd$_modules["focus"]["handle_focus_out"] = handle_focus_out;

        _$rapyd$_modules["focus"]["get_editable_text"] = get_editable_text;

        _$rapyd$_modules["focus"]["set_editable_text"] = set_editable_text;

        _$rapyd$_modules["focus"]["onload"] = onload;
    })();

    (function(){
        var __name__ = "elementmaker";
        var html_elements, mathml_elements, svg_elements, html5_tags, create_element, create_text_node, tag;
        html_elements = (function(){
            var s = _$rapyd$_set();
            s.jsset.add("a");
            s.jsset.add("abbr");
            s.jsset.add("acronym");
            s.jsset.add("address");
            s.jsset.add("area");
            s.jsset.add("article");
            s.jsset.add("aside");
            s.jsset.add("audio");
            s.jsset.add("b");
            s.jsset.add("big");
            s.jsset.add("blockquote");
            s.jsset.add("br");
            s.jsset.add("button");
            s.jsset.add("canvas");
            s.jsset.add("caption");
            s.jsset.add("center");
            s.jsset.add("cite");
            s.jsset.add("code");
            s.jsset.add("col");
            s.jsset.add("colgroup");
            s.jsset.add("command");
            s.jsset.add("datagrid");
            s.jsset.add("datalist");
            s.jsset.add("dd");
            s.jsset.add("del");
            s.jsset.add("details");
            s.jsset.add("dfn");
            s.jsset.add("dialog");
            s.jsset.add("dir");
            s.jsset.add("div");
            s.jsset.add("dl");
            s.jsset.add("dt");
            s.jsset.add("em");
            s.jsset.add("event-source");
            s.jsset.add("fieldset");
            s.jsset.add("figcaption");
            s.jsset.add("figure");
            s.jsset.add("footer");
            s.jsset.add("font");
            s.jsset.add("form");
            s.jsset.add("header");
            s.jsset.add("h1");
            s.jsset.add("h2");
            s.jsset.add("h3");
            s.jsset.add("h4");
            s.jsset.add("h5");
            s.jsset.add("h6");
            s.jsset.add("hr");
            s.jsset.add("i");
            s.jsset.add("img");
            s.jsset.add("input");
            s.jsset.add("ins");
            s.jsset.add("keygen");
            s.jsset.add("kbd");
            s.jsset.add("label");
            s.jsset.add("legend");
            s.jsset.add("li");
            s.jsset.add("m");
            s.jsset.add("map");
            s.jsset.add("menu");
            s.jsset.add("meter");
            s.jsset.add("multicol");
            s.jsset.add("nav");
            s.jsset.add("nextid");
            s.jsset.add("ol");
            s.jsset.add("output");
            s.jsset.add("optgroup");
            s.jsset.add("option");
            s.jsset.add("p");
            s.jsset.add("pre");
            s.jsset.add("progress");
            s.jsset.add("q");
            s.jsset.add("s");
            s.jsset.add("samp");
            s.jsset.add("script");
            s.jsset.add("section");
            s.jsset.add("select");
            s.jsset.add("small");
            s.jsset.add("sound");
            s.jsset.add("source");
            s.jsset.add("spacer");
            s.jsset.add("span");
            s.jsset.add("strike");
            s.jsset.add("strong");
            s.jsset.add("style");
            s.jsset.add("sub");
            s.jsset.add("sup");
            s.jsset.add("table");
            s.jsset.add("tbody");
            s.jsset.add("td");
            s.jsset.add("textarea");
            s.jsset.add("time");
            s.jsset.add("tfoot");
            s.jsset.add("th");
            s.jsset.add("thead");
            s.jsset.add("tr");
            s.jsset.add("tt");
            s.jsset.add("u");
            s.jsset.add("ul");
            s.jsset.add("var");
            s.jsset.add("video");
            return s;
        })();
        mathml_elements = (function(){
            var s = _$rapyd$_set();
            s.jsset.add("maction");
            s.jsset.add("math");
            s.jsset.add("merror");
            s.jsset.add("mfrac");
            s.jsset.add("mi");
            s.jsset.add("mmultiscripts");
            s.jsset.add("mn");
            s.jsset.add("mo");
            s.jsset.add("mover");
            s.jsset.add("mpadded");
            s.jsset.add("mphantom");
            s.jsset.add("mprescripts");
            s.jsset.add("mroot");
            s.jsset.add("mrow");
            s.jsset.add("mspace");
            s.jsset.add("msqrt");
            s.jsset.add("mstyle");
            s.jsset.add("msub");
            s.jsset.add("msubsup");
            s.jsset.add("msup");
            s.jsset.add("mtable");
            s.jsset.add("mtd");
            s.jsset.add("mtext");
            s.jsset.add("mtr");
            s.jsset.add("munder");
            s.jsset.add("munderover");
            s.jsset.add("none");
            return s;
        })();
        svg_elements = (function(){
            var s = _$rapyd$_set();
            s.jsset.add("a");
            s.jsset.add("animate");
            s.jsset.add("animateColor");
            s.jsset.add("animateMotion");
            s.jsset.add("animateTransform");
            s.jsset.add("clipPath");
            s.jsset.add("circle");
            s.jsset.add("defs");
            s.jsset.add("desc");
            s.jsset.add("ellipse");
            s.jsset.add("font-face");
            s.jsset.add("font-face-name");
            s.jsset.add("font-face-src");
            s.jsset.add("g");
            s.jsset.add("glyph");
            s.jsset.add("hkern");
            s.jsset.add("linearGradient");
            s.jsset.add("line");
            s.jsset.add("marker");
            s.jsset.add("metadata");
            s.jsset.add("missing-glyph");
            s.jsset.add("mpath");
            s.jsset.add("path");
            s.jsset.add("polygon");
            s.jsset.add("polyline");
            s.jsset.add("radialGradient");
            s.jsset.add("rect");
            s.jsset.add("set");
            s.jsset.add("stop");
            s.jsset.add("svg");
            s.jsset.add("switch");
            s.jsset.add("text");
            s.jsset.add("title");
            s.jsset.add("tspan");
            s.jsset.add("use");
            return s;
        })();
        html5_tags = html_elements.union(mathml_elements).union(svg_elements);
        function _dummy_create_element(name) {
            return {
                "name": name,
                "children": _$rapyd$_list_decorate([]),
                "attributes": {},
                "setAttribute": function(name, val) {
                    this.attributes[name] = val;
                },
                "appendChild": function(child) {
                    this.children.push(child);
                }
            };
        }
        function _dummy_create_text(value) {
            return value;
        }
        if (typeof document === "undefined") {
            create_element = _dummy_create_element;
            create_text_node = _dummy_create_text;
        } else {
            create_element = function(name) {
                return document.createElement(name);
            };
            create_text_node = function(val) {
                return document.createTextNode(val);
            };
        }
        function E() {
            var tag = ( 0 === arguments.length-1 && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [_$rapyd$_kwargs_symbol] === true) ? undefined : arguments[0];
            var kwargs = arguments[arguments.length-1];
            if (typeof kwargs !== "object" || kwargs [_$rapyd$_kwargs_symbol] !== true) kwargs = {};
            var args = Array.prototype.slice.call(arguments, 1 );
            if (typeof kwargs === "object" && kwargs [_$rapyd$_kwargs_symbol] === true) args .pop();
            var ans, vattr, attr, arg;
            ans = create_element(tag);
            var _$rapyd$_Iter0 = _$rapyd$_Iterable(kwargs);
            for (var _$rapyd$_Index0 = 0; _$rapyd$_Index0 < _$rapyd$_Iter0.length; _$rapyd$_Index0++) {
                attr = _$rapyd$_Iter0[_$rapyd$_Index0];
                vattr = str.replace(str.rstrip(attr, "_"), "_", "-");
                ans.setAttribute(vattr, kwargs[attr]);
            }
            var _$rapyd$_Iter1 = _$rapyd$_Iterable(args);
            for (var _$rapyd$_Index1 = 0; _$rapyd$_Index1 < _$rapyd$_Iter1.length; _$rapyd$_Index1++) {
                arg = _$rapyd$_Iter1[_$rapyd$_Index1];
                if (typeof arg === "string") {
                    ans.appendChild(create_text_node(arg));
                } else {
                    ans.appendChild(arg);
                }
            }
            return ans;
        }
        function bind_e(tag) {
            return function() {
                var kwargs = arguments[arguments.length-1];
                if (typeof kwargs !== "object" || kwargs [_$rapyd$_kwargs_symbol] !== true) kwargs = {};
                var args = Array.prototype.slice.call(arguments, 0 );
                if (typeof kwargs === "object" && kwargs [_$rapyd$_kwargs_symbol] === true) args .pop();
                return E.apply(this, [tag].concat(args).concat([_$rapyd$_desugar_kwargs(kwargs)]));
            };
        }
        var _$rapyd$_Iter2 = _$rapyd$_Iterable(html5_tags);
        for (var _$rapyd$_Index2 = 0; _$rapyd$_Index2 < _$rapyd$_Iter2.length; _$rapyd$_Index2++) {
            tag = _$rapyd$_Iter2[_$rapyd$_Index2];
            Object.defineProperty(E, tag, {
                "value": bind_e(tag)
            });
        }
        _$rapyd$_modules["elementmaker"]["html_elements"] = html_elements;

        _$rapyd$_modules["elementmaker"]["mathml_elements"] = mathml_elements;

        _$rapyd$_modules["elementmaker"]["svg_elements"] = svg_elements;

        _$rapyd$_modules["elementmaker"]["html5_tags"] = html5_tags;

        _$rapyd$_modules["elementmaker"]["create_element"] = create_element;

        _$rapyd$_modules["elementmaker"]["create_text_node"] = create_text_node;

        _$rapyd$_modules["elementmaker"]["tag"] = tag;

        _$rapyd$_modules["elementmaker"]["_dummy_create_element"] = _dummy_create_element;

        _$rapyd$_modules["elementmaker"]["_dummy_create_text"] = _dummy_create_text;

        _$rapyd$_modules["elementmaker"]["E"] = E;

        _$rapyd$_modules["elementmaker"]["bind_e"] = bind_e;
    })();

    (function(){
        var __name__ = "humanize";
        var LABELS;
        function normalize_precision(value, base) {
            value = Math.round(Math.abs(value));
            return (isNaN(value)) ? base : value;
        }
        function to_fixed(value, precision) {
            var power;
            precision = precision || normalize_precision(precision, 0);
            power = Math.pow(10, precision);
            return (Math.round(value * power) / power).toFixed(precision);
        }
        function humanize_number(number, precision, thousand, decimal) {
            var use_precision, negative, base, mod;
            precision = precision || 0;
            thousand = thousand || ",";
            decimal = decimal || ".";
            function first_comma(number, position) {
                return (position) ? number.substr(0, position) + thousand : "";
            }
            function commas(number, position) {
                return number.substr(position).replace(/(\d{3})(?=\d)/g, "$1" + thousand);
            }
            function decimals(number, use_precision) {
                return (use_precision) ? decimal + to_fixed(Math.abs(number), use_precision).split(".")[1] : "";
            }
            use_precision = normalize_precision(precision);
            negative = (number < 0) ? "-" : "";
            base = parseInt(to_fixed(Math.abs(number || 0), use_precision), 10) + "";
            mod = (base.length > 3) ? base.length % 3 : 0;
            return negative + first_comma(base, mod) + commas(base, mod) + decimals(number, use_precision);
        }
        LABELS = _$rapyd$_list_decorate([ _$rapyd$_list_decorate([ "P", Math.pow(2, 50) ]), _$rapyd$_list_decorate([ "T", Math.pow(2, 40) ]), _$rapyd$_list_decorate([ "G", 1 << 30 ]), _$rapyd$_list_decorate([ "M", 1 << 20 ]) ]);
        function humanize_size(size) {
            var _$rapyd$_Unpack, label, minnum;
            var _$rapyd$_Iter0 = _$rapyd$_Iterable(LABELS);
            for (var _$rapyd$_Index0 = 0; _$rapyd$_Index0 < _$rapyd$_Iter0.length; _$rapyd$_Index0++) {
                _$rapyd$_Unpack = _$rapyd$_Iter0[_$rapyd$_Index0];
                label = _$rapyd$_Unpack[0];
                minnum = _$rapyd$_Unpack[1];
                if (size >= minnum) {
                    return humanize_number(size / minnum, 2, "") + " " + label + "B";
                }
            }
            if (size >= 1024) {
                return humanize_number(size / 1024, 0) + " KB";
            }
            return humanize_number(size, 0) + " B";
        }
        function relative_time(timestamp) {
            var current_time, time_diff, days2, days29, days60, cur_years, ts_years, cur_months, ts_months, month_diff, year_diff;
            timestamp = timestamp || Date.now();
            current_time = Date.now() / 1e3;
            time_diff = current_time - timestamp / 1e3;
            if (time_diff < 2 && time_diff > -2) {
                return ((time_diff >= 0) ? "just " : "") + "now";
            }
            if (time_diff < 60 && time_diff > -60) {
                return (time_diff >= 0) ? Math.floor(time_diff) + " seconds ago" : "in " + Math.floor(-time_diff) + " seconds";
            }
            if (time_diff < 120 && time_diff > -120) {
                return (time_diff >= 0) ? "about a minute ago" : "in about a minute";
            }
            if (time_diff < 3600 && time_diff > -3600) {
                return (time_diff >= 0) ? Math.floor(time_diff / 60) + " minutes ago" : "in " + Math.floor(-time_diff / 60) + " minutes";
            }
            if (time_diff < 7200 && time_diff > -7200) {
                return (time_diff >= 0) ? "about an hour ago" : "in about an hour";
            }
            if (time_diff < 86400 && time_diff > -86400) {
                return (time_diff >= 0) ? Math.floor(time_diff / 3600) + " hours ago" : "in " + Math.floor(-time_diff / 3600) + " hours";
            }
            days2 = 2 * 86400;
            if (time_diff < days2 && time_diff > -days2) {
                return (time_diff >= 0) ? "1 day ago" : "in 1 day";
            }
            days29 = 29 * 86400;
            if (time_diff < days29 && time_diff > -days29) {
                return (time_diff >= 0) ? Math.floor(time_diff / 86400) + " days ago" : "in " + Math.floor(-time_diff / 86400) + " days";
            }
            days60 = 60 * 86400;
            if (time_diff < days60 && time_diff > -days60) {
                return (time_diff >= 0) ? "about a month ago" : "in about a month";
            }
            cur_years = new Date(current_time * 1e3).getFullYear();
            ts_years = new Date(timestamp).getFullYear();
            cur_months = new Date(current_time * 1e3).getMonth() + 1 + 12 * cur_years;
            ts_months = new Date(timestamp).getMonth() + 1 + 12 * cur_years;
            month_diff = cur_months - ts_months;
            if (month_diff < 12 && month_diff > -12) {
                return (month_diff >= 0) ? month_diff + " months ago" : "in " + -month_diff + " months";
            }
            year_diff = cur_years - ts_years;
            if (year_diff < 2 && year_diff > -2) {
                return (year_diff >= 0) ? "a year ago" : "in a year";
            }
            return (year_diff >= 0) ? year_diff + " years ago" : "in " + -year_diff + " years";
        }
        _$rapyd$_modules["humanize"]["LABELS"] = LABELS;

        _$rapyd$_modules["humanize"]["normalize_precision"] = normalize_precision;

        _$rapyd$_modules["humanize"]["to_fixed"] = to_fixed;

        _$rapyd$_modules["humanize"]["humanize_number"] = humanize_number;

        _$rapyd$_modules["humanize"]["humanize_size"] = humanize_size;

        _$rapyd$_modules["humanize"]["relative_time"] = relative_time;
    })();

    (function(){
        var __name__ = "downloads";
        var E = _$rapyd$_modules["elementmaker"].E;
        
        var humanize_size = _$rapyd$_modules["humanize"].humanize_size;
        var relative_time = _$rapyd$_modules["humanize"].relative_time;
        
        var callback = _$rapyd$_modules["qt"].callback;
        
        function cancel_download(dl_id) {
            callback("downloads", {
                "id": int(dl_id),
                "cmd": "cancel"
            });
        }
        function open_download(dl_id) {
            callback("downloads", {
                "id": int(dl_id),
                "cmd": "open"
            });
        }
        function create_download(dl_id, fname, mime_type, icon_url, hostname) {
            var div, stop;
            document.getElementById("init").style.display = "none";
            div = E.div(E.img(_$rapyd$_desugar_kwargs({src: icon_url, alt: fname, style: "width: 64px; height: 64px; margin-right: 1em; float:left; display:table-cell"})), E.div(E.p(E.b(fname, _$rapyd$_desugar_kwargs({id: "fname" + dl_id})), E.br(), E.span("...", _$rapyd$_desugar_kwargs({id: "status" + dl_id, style: "color:gray", data_hostname: hostname, data_created: Date.now() + ""}))), _$rapyd$_desugar_kwargs({style: "float:left; display:table-cell"})), E.div(E.br(), E.span("✖ ", _$rapyd$_desugar_kwargs({class_: "stop", style: "font-size: x-large; cursor:pointer", title: "Stop download"})), _$rapyd$_desugar_kwargs({id: "stop" + dl_id, style: "float:right;"})), _$rapyd$_desugar_kwargs({style: "padding: 3ex; display: table; width: 90%; border-bottom: solid 1px currentColor"}));
            document.body.insertBefore(div, document.body.firstChild);
            update_download(dl_id, "running", -1, -1, 0);
            stop = document.getElementById("stop" + dl_id);
            stop.addEventListener("click", function() {
                cancel_download(dl_id);
            });
        }
        function update_download(dl_id, state, received, total, rate) {
            var status, h, left, fname, text, stop;
            status = document.getElementById("status" + dl_id);
            h = humanize_size;
            if (state === "running") {
                if (received > -1 && total > -1) {
                    if (rate > 0) {
                        left = relative_time(Date.now() + 1e3 * ((total - received) / rate));
                        status.innerText = str.format("{recv} of {total} at {rate}/s — Will finish {left}", _$rapyd$_desugar_kwargs({recv: h(received), total: h(total), rate: h(rate), left: left}));
                    } else {
                        left = (rate < 0) ? "Estimating time remaining" : "Stalled";
                        status.innerText = str.format("{recv} of {total} — {left}", _$rapyd$_desugar_kwargs({recv: h(received), total: h(total), left: left}));
                    }
                } else {
                    status.innerText = "Downloading, please wait...";
                }
            } else if (state === "completed") {
                fname = document.getElementById("fname" + dl_id);
                if (fname) {
                    if (!fname.getAttribute("class")) {
                        fname.addEventListener("click", function() {
                            open_download(dl_id);
                        });
                    }
                    fname.setAttribute("class", "fname");
                    fname.setAttribute("title", "Click to open");
                }
                text = "";
                if (total > -1) {
                    text += h(total) + " — ";
                }
                text += status.getAttribute("data-hostname") + " — ";
                text += "Completed";
                if (total > -1) {
                    rate = 1e3 * total / (Date.now() - int(status.getAttribute("data-created")));
                    text += " at " + h(rate) + "/s";
                }
                status.innerText = text;
            } else {
                text = (state === "canceled") ? "Canceled" : "Interrupted";
                text += " — " + status.getAttribute("data-hostname");
                status.innerText = text;
            }
            stop = document.getElementById("stop" + dl_id);
            stop.style.display = (state === "running") ? "block" : "none";
        }
        function main() {
            window.create_download = create_download;
            window.update_download = update_download;
            document.getElementsByTagName("style")[0].innerText = "\n    body { color: black; background-color: #eee; }\n    .stop:hover { color: red }\n    .fname { cursor: pointer }\n    .fname:hover { color: red; font-style: italic }\n    ";
            callback("downloads", {
                "cmd": "inited"
            });
        }
        _$rapyd$_modules["downloads"]["cancel_download"] = cancel_download;

        _$rapyd$_modules["downloads"]["open_download"] = open_download;

        _$rapyd$_modules["downloads"]["create_download"] = create_download;

        _$rapyd$_modules["downloads"]["update_download"] = update_download;

        _$rapyd$_modules["downloads"]["main"] = main;
    })();

    (function(){

        var __name__ = "__main__";


        var connect_bridge = _$rapyd$_modules["qt"].connect_bridge;
        
        var mc_onload = _$rapyd$_modules["middle_click"].onload;
        
        var focus_onload = _$rapyd$_modules["focus"].onload;
        
        var downloads = _$rapyd$_modules["downloads"].main;
        
        function on_document_loaded() {
            connect_bridge(function() {
                mc_onload();
                focus_onload();
                if (typeof window["ͻ-vise-entry-point"] === "function") {
                    window["ͻ-vise-entry-point"](vise_entry_point);
                }
            });
        }
        function vise_entry_point(name) {
            if (name === "downloads") {
                downloads();
            }
        }
        document.removeEventListener("DOMContentLoaded", on_document_loaded);
        document.addEventListener("DOMContentLoaded", on_document_loaded);
    })();
})();
