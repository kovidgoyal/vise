(function(){
    "use strict";
    var _$rapyd$_iterator_symbol = (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") ? Symbol.iterator : "iterator-Symbol-5d0927e5554349048cf0e3762a228256";
    var _$rapyd$_kwargs_symbol = (typeof Symbol === "function") ? Symbol("kwargs-object") : "kwargs-object-Symbol-5d0927e5554349048cf0e3762a228256";
    var _$rapyd$_cond_temp;
    var _$rapyd$_object_counter = 0;
    function _$rapyd$_Iterable(iterable) {
            var iterator, ans, result;
            if (_$rapyd$_arraylike(iterable)) {
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
            return Object.keys(iterable);
        };
    function _$rapyd$_extends(child, parent) {
            child.prototype = Object.create(parent.prototype);
            child.prototype.constructor = child;
        };
    var _$rapyd$_in = (function _$rapyd$_in() {
            if (typeof Map === "function" && typeof Set === "function") {
                return function(val, arr) {
                    if (typeof arr === "string") {
                        return arr.indexOf(val) !== -1;
                    }
                    if (typeof arr.__contains__ === "function") {
                        return arr.__contains__(val);
                    }
                    if ((arr instanceof Map || arr instanceof Set)) {
                        return arr.has(val);
                    }
                    if (_$rapyd$_arraylike(arr)) {
                        return _$rapyd$_list_contains.call(arr, val);
                    }
                    return Object.prototype.hasOwnProperty.call(arr, val);
                };
            }
            return function(val, arr) {
                if (typeof arr === "string") {
                    return arr.indexOf(val) !== -1;
                }
                if (typeof arr.__contains__ === "function") {
                    return arr.__contains__(val);
                }
                if (_$rapyd$_arraylike(arr)) {
                    return _$rapyd$_list_contains.call(arr, val);
                }
                return Object.prototype.hasOwnProperty.call(arr, val);
            };
        })();
    var len = (function _$rapyd$_len() {
            if (typeof Set === "function" && typeof Map === "function") {
                return function(obj) {
                    if (_$rapyd$_arraylike(obj)) {
                        return obj.length;
                    }
                    if (obj instanceof Set || obj instanceof Map) {
                        return obj.size;
                    }
                    if (typeof obj.__len__ === "function") {
                        return obj.__len__();
                    }
                    return Object.keys(obj).length;
                };
            }
            return function(obj) {
                if (_$rapyd$_arraylike(obj)) {
                    return obj.length;
                }
                if (typeof obj.__len__ === "function") {
                    return obj.__len__();
                }
                return Object.keys(obj).length;
            };
        })();
    function range(start, stop, step) {
            var length;
            if (arguments.length <= 1) {
                stop = start || 0;
                start = 0;
            }
            step = arguments[2] || 1;
            length = Math.max(Math.ceil((stop - start) / step), 0);
            return (function(){
                var _$rapyd$_d = {};
                _$rapyd$_d[_$rapyd$_iterator_symbol] = function() {
                    return this;
                };
                _$rapyd$_d["_i"] = start - step;
                _$rapyd$_d["_idx"] = -1;
                _$rapyd$_d["next"] = function() {
                    this._i += step;
                    this._idx += 1;
                    if (this._idx >= length) {
                        return {
                            "done": true
                        };
                    }
                    return {
                        "done": false,
                        "value": this._i
                    };
                };
                return _$rapyd$_d;
            })();
        };
    var _$rapyd$_desugar_kwargs = (function _$rapyd$_desugar_kwargs() {
            if (typeof Object.assign === "function") {
                return function() {
                    var ans;
                    ans = {};
                    ans[_$rapyd$_kwargs_symbol] = true;
                    for (var i = 0; i < arguments.length; i++) {
                        Object.assign(ans, arguments[i]);
                    }
                    return ans;
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
    var _$rapyd$_regenerator = {};
    !(function(global) {
      "use strict";
    
      var hasOwn = Object.prototype.hasOwnProperty;
      var undefined; 
    
      var iteratorSymbol =
        typeof Symbol === "function" && Symbol.iterator || "@@iterator";
    
      var inModule = typeof module === "object";
      var runtime = global.regeneratorRuntime;
      if (runtime) {
        if (inModule) {
    
          module.exports = runtime;
        }
    
        return;
      }
    
      runtime = global.regeneratorRuntime = inModule ? module.exports : {};
    
      function wrap(innerFn, outerFn, self, tryLocsList) {
    
        var generator = Object.create((outerFn || Generator).prototype);
    
        generator._invoke = makeInvokeMethod(
          innerFn, self || null,
          new Context(tryLocsList || [])
        );
    
        return generator;
      }
      runtime.wrap = wrap;
    
      function tryCatch(fn, obj, arg) {
        try {
          return { type: "normal", arg: fn.call(obj, arg) };
        } catch (err) {
          return { type: "throw", arg: err };
        }
      }
    
      var GenStateSuspendedStart = "suspendedStart";
      var GenStateSuspendedYield = "suspendedYield";
      var GenStateExecuting = "executing";
      var GenStateCompleted = "completed";
    
      var ContinueSentinel = {};
    
      function Generator() {}
      function GeneratorFunction() {}
      function GeneratorFunctionPrototype() {}
    
      var Gp = GeneratorFunctionPrototype.prototype = Generator.prototype;
      GeneratorFunction.prototype = Gp.constructor = GeneratorFunctionPrototype;
      GeneratorFunctionPrototype.constructor = GeneratorFunction;
      GeneratorFunction.displayName = "GeneratorFunction";
    
      function defineIteratorMethods(prototype) {
        ["next", "throw", "return"].forEach(function(method) {
          prototype[method] = function(arg) {
            return this._invoke(method, arg);
          };
        });
      }
    
      runtime.isGeneratorFunction = function(genFun) {
        var ctor = typeof genFun === "function" && genFun.constructor;
        return ctor
          ? ctor === GeneratorFunction ||
    
            (ctor.displayName || ctor.name) === "GeneratorFunction"
          : false;
      };
    
      runtime.mark = function(genFun) {
        genFun.__proto__ = GeneratorFunctionPrototype;
        genFun.prototype = Object.create(Gp);
        return genFun;
      };
    
      runtime.awrap = function(arg) {
        return new AwaitArgument(arg);
      };
    
      function AwaitArgument(arg) {
        this.arg = arg;
      }
    
      function AsyncIterator(generator) {
    
        function invoke(method, arg) {
          var result = generator[method](arg);
          var value = result.value;
          return value instanceof AwaitArgument
            ? Promise.resolve(value.arg).then(invokeNext, invokeThrow)
            : Promise.resolve(value).then(function(unwrapped) {
    
                result.value = unwrapped;
                return result;
              });
        }
    
        if (typeof process === "object" && process.domain) {
          invoke = process.domain.bind(invoke);
        }
    
        var invokeNext = invoke.bind(generator, "next");
        var invokeThrow = invoke.bind(generator, "throw");
        var invokeReturn = invoke.bind(generator, "return");
        var previousPromise;
    
        function enqueue(method, arg) {
          var enqueueResult =
    
            previousPromise ? previousPromise.then(function() {
              return invoke(method, arg);
            }) : new Promise(function(resolve) {
              resolve(invoke(method, arg));
            });
    
          previousPromise = enqueueResult["catch"](function(ignored){});
    
          return enqueueResult;
        }
    
        this._invoke = enqueue;
      }
    
      defineIteratorMethods(AsyncIterator.prototype);
    
      runtime.async = function(innerFn, outerFn, self, tryLocsList) {
        var iter = new AsyncIterator(
          wrap(innerFn, outerFn, self, tryLocsList)
        );
    
        return runtime.isGeneratorFunction(outerFn)
          ? iter 
    
          : iter.next().then(function(result) {
              return result.done ? result.value : iter.next();
            });
      };
    
      function makeInvokeMethod(innerFn, self, context) {
        var state = GenStateSuspendedStart;
    
        return function invoke(method, arg) {
          if (state === GenStateExecuting) {
            throw new Error("Generator is already running");
          }
    
          if (state === GenStateCompleted) {
            if (method === "throw") {
              throw arg;
            }
    
            return doneResult();
          }
    
          while (true) {
            var delegate = context.delegate;
            if (delegate) {
              if (method === "return" ||
                  (method === "throw" && delegate.iterator[method] === undefined)) {
    
                context.delegate = null;
    
                var returnMethod = delegate.iterator["return"];
                if (returnMethod) {
                  var record = tryCatch(returnMethod, delegate.iterator, arg);
                  if (record.type === "throw") {
    
                    method = "throw";
                    arg = record.arg;
                    continue;
                  }
                }
    
                if (method === "return") {
    
                  continue;
                }
              }
    
              var record = tryCatch(
                delegate.iterator[method],
                delegate.iterator,
                arg
              );
    
              if (record.type === "throw") {
                context.delegate = null;
    
                method = "throw";
                arg = record.arg;
                continue;
              }
    
              method = "next";
              arg = undefined;
    
              var info = record.arg;
              if (info.done) {
                context[delegate.resultName] = info.value;
                context.next = delegate.nextLoc;
              } else {
                state = GenStateSuspendedYield;
                return info;
              }
    
              context.delegate = null;
            }
    
            if (method === "next") {
              if (state === GenStateSuspendedYield) {
                context.sent = arg;
              } else {
                context.sent = undefined;
              }
    
            } else if (method === "throw") {
              if (state === GenStateSuspendedStart) {
                state = GenStateCompleted;
                throw arg;
              }
    
              if (context.dispatchException(arg)) {
    
                method = "next";
                arg = undefined;
              }
    
            } else if (method === "return") {
              context.abrupt("return", arg);
            }
    
            state = GenStateExecuting;
    
            var record = tryCatch(innerFn, self, context);
            if (record.type === "normal") {
    
              state = context.done
                ? GenStateCompleted
                : GenStateSuspendedYield;
    
              var info = {
                value: record.arg,
                done: context.done
              };
    
              if (record.arg === ContinueSentinel) {
                if (context.delegate && method === "next") {
    
                  arg = undefined;
                }
              } else {
                return info;
              }
    
            } else if (record.type === "throw") {
              state = GenStateCompleted;
    
              method = "throw";
              arg = record.arg;
            }
          }
        };
      }
    
      defineIteratorMethods(Gp);
    
      Gp[iteratorSymbol] = function() {
        return this;
      };
    
      Gp.toString = function() {
        return "[object Generator]";
      };
    
      function pushTryEntry(locs) {
        var entry = { tryLoc: locs[0] };
    
        if (1 in locs) {
          entry.catchLoc = locs[1];
        }
    
        if (2 in locs) {
          entry.finallyLoc = locs[2];
          entry.afterLoc = locs[3];
        }
    
        this.tryEntries.push(entry);
      }
    
      function resetTryEntry(entry) {
        var record = entry.completion || {};
        record.type = "normal";
        delete record.arg;
        entry.completion = record;
      }
    
      function Context(tryLocsList) {
    
        this.tryEntries = [{ tryLoc: "root" }];
        tryLocsList.forEach(pushTryEntry, this);
        this.reset(true);
      }
    
      runtime.keys = function(object) {
        var keys = [];
        for (var key in object) {
          keys.push(key);
        }
        keys.reverse();
    
        return function next() {
          while (keys.length) {
            var key = keys.pop();
            if (key in object) {
              next.value = key;
              next.done = false;
              return next;
            }
          }
    
          next.done = true;
          return next;
        };
      };
    
      function values(iterable) {
        if (iterable) {
          var iteratorMethod = iterable[iteratorSymbol];
          if (iteratorMethod) {
            return iteratorMethod.call(iterable);
          }
    
          if (typeof iterable.next === "function") {
            return iterable;
          }
    
          if (!isNaN(iterable.length)) {
            var i = -1, next = function next() {
              while (++i < iterable.length) {
                if (hasOwn.call(iterable, i)) {
                  next.value = iterable[i];
                  next.done = false;
                  return next;
                }
              }
    
              next.value = undefined;
              next.done = true;
    
              return next;
            };
    
            return next.next = next;
          }
        }
    
        return { next: doneResult };
      }
      runtime.values = values;
    
      function doneResult() {
        return { value: undefined, done: true };
      }
    
      Context.prototype = {
        constructor: Context,
    
        reset: function(skipTempReset) {
          this.prev = 0;
          this.next = 0;
          this.sent = undefined;
          this.done = false;
          this.delegate = null;
    
          this.tryEntries.forEach(resetTryEntry);
    
          if (!skipTempReset) {
            for (var name in this) {
    
              if (name.charAt(0) === "t" &&
                  hasOwn.call(this, name) &&
                  !isNaN(+name.slice(1))) {
                this[name] = undefined;
              }
            }
          }
        },
    
        stop: function() {
          this.done = true;
    
          var rootEntry = this.tryEntries[0];
          var rootRecord = rootEntry.completion;
          if (rootRecord.type === "throw") {
            throw rootRecord.arg;
          }
    
          return this.rval;
        },
    
        dispatchException: function(exception) {
          if (this.done) {
            throw exception;
          }
    
          var context = this;
          function handle(loc, caught) {
            record.type = "throw";
            record.arg = exception;
            context.next = loc;
            return !!caught;
          }
    
          for (var i = this.tryEntries.length - 1; i >= 0; --i) {
            var entry = this.tryEntries[i];
            var record = entry.completion;
    
            if (entry.tryLoc === "root") {
    
              return handle("end");
            }
    
            if (entry.tryLoc <= this.prev) {
              var hasCatch = hasOwn.call(entry, "catchLoc");
              var hasFinally = hasOwn.call(entry, "finallyLoc");
    
              if (hasCatch && hasFinally) {
                if (this.prev < entry.catchLoc) {
                  return handle(entry.catchLoc, true);
                } else if (this.prev < entry.finallyLoc) {
                  return handle(entry.finallyLoc);
                }
    
              } else if (hasCatch) {
                if (this.prev < entry.catchLoc) {
                  return handle(entry.catchLoc, true);
                }
    
              } else if (hasFinally) {
                if (this.prev < entry.finallyLoc) {
                  return handle(entry.finallyLoc);
                }
    
              } else {
                throw new Error("try statement without catch or finally");
              }
            }
          }
        },
    
        abrupt: function(type, arg) {
          for (var i = this.tryEntries.length - 1; i >= 0; --i) {
            var entry = this.tryEntries[i];
            if (entry.tryLoc <= this.prev &&
                hasOwn.call(entry, "finallyLoc") &&
                this.prev < entry.finallyLoc) {
              var finallyEntry = entry;
              break;
            }
          }
    
          if (finallyEntry &&
              (type === "break" ||
               type === "continue") &&
              finallyEntry.tryLoc <= arg &&
              arg <= finallyEntry.finallyLoc) {
    
            finallyEntry = null;
          }
    
          var record = finallyEntry ? finallyEntry.completion : {};
          record.type = type;
          record.arg = arg;
    
          if (finallyEntry) {
            this.next = finallyEntry.finallyLoc;
          } else {
            this.complete(record);
          }
    
          return ContinueSentinel;
        },
    
        complete: function(record, afterLoc) {
          if (record.type === "throw") {
            throw record.arg;
          }
    
          if (record.type === "break" ||
              record.type === "continue") {
            this.next = record.arg;
          } else if (record.type === "return") {
            this.rval = record.arg;
            this.next = "end";
          } else if (record.type === "normal" && afterLoc) {
            this.next = afterLoc;
          }
        },
    
        finish: function(finallyLoc) {
          for (var i = this.tryEntries.length - 1; i >= 0; --i) {
            var entry = this.tryEntries[i];
            if (entry.finallyLoc === finallyLoc) {
              this.complete(entry.completion, entry.afterLoc);
              resetTryEntry(entry);
              return ContinueSentinel;
            }
          }
        },
    
        "catch": function(tryLoc) {
          for (var i = this.tryEntries.length - 1; i >= 0; --i) {
            var entry = this.tryEntries[i];
            if (entry.tryLoc === tryLoc) {
              var record = entry.completion;
              if (record.type === "throw") {
                var thrown = record.arg;
                resetTryEntry(entry);
              }
              return thrown;
            }
          }
    
          throw new Error("illegal catch attempt");
        },
    
        delegateYield: function(iterable, resultName, nextLoc) {
          this.delegate = {
            iterator: values(iterable),
            resultName: resultName,
            nextLoc: nextLoc
          };
    
          return ContinueSentinel;
        }
      };
    })(_$rapyd$_regenerator);
    function callable(x) {
            return typeof x === "function";
        };
    var Exception = Error;
function AttributeError() {
    if (this._$rapyd$_object_id === undefined) Object.defineProperty(this, "_$rapyd$_object_id", {"value":++_$rapyd$_object_counter});
    AttributeError.prototype.__init__.apply(this, arguments);
}
_$rapyd$_extends(AttributeError, Error);
AttributeError.prototype.__init__ = function __init__(msg) {
    var self = this;
    self.message = msg;
    self.stack = new Error().stack;
};
AttributeError.prototype.__repr__ = function __repr__ () {
    return "<" + __name__ + "." + "AttributeError" + " #" + this._$rapyd$_object_id + ">";
};
AttributeError.prototype.__str__ = function __str__ () {
    return this.__repr__();
};
AttributeError.prototype.name = "AttributeError";

function IndexError() {
    if (this._$rapyd$_object_id === undefined) Object.defineProperty(this, "_$rapyd$_object_id", {"value":++_$rapyd$_object_counter});
    IndexError.prototype.__init__.apply(this, arguments);
}
_$rapyd$_extends(IndexError, Error);
IndexError.prototype.__init__ = function __init__(msg) {
    var self = this;
    self.message = msg;
    self.stack = new Error().stack;
};
IndexError.prototype.__repr__ = function __repr__ () {
    return "<" + __name__ + "." + "IndexError" + " #" + this._$rapyd$_object_id + ">";
};
IndexError.prototype.__str__ = function __str__ () {
    return this.__repr__();
};
IndexError.prototype.name = "IndexError";

function KeyError() {
    if (this._$rapyd$_object_id === undefined) Object.defineProperty(this, "_$rapyd$_object_id", {"value":++_$rapyd$_object_counter});
    KeyError.prototype.__init__.apply(this, arguments);
}
_$rapyd$_extends(KeyError, Error);
KeyError.prototype.__init__ = function __init__(msg) {
    var self = this;
    self.message = msg;
    self.stack = new Error().stack;
};
KeyError.prototype.__repr__ = function __repr__ () {
    return "<" + __name__ + "." + "KeyError" + " #" + this._$rapyd$_object_id + ">";
};
KeyError.prototype.__str__ = function __str__ () {
    return this.__repr__();
};
KeyError.prototype.name = "KeyError";

function ValueError() {
    if (this._$rapyd$_object_id === undefined) Object.defineProperty(this, "_$rapyd$_object_id", {"value":++_$rapyd$_object_counter});
    ValueError.prototype.__init__.apply(this, arguments);
}
_$rapyd$_extends(ValueError, Error);
ValueError.prototype.__init__ = function __init__(msg) {
    var self = this;
    self.message = msg;
    self.stack = new Error().stack;
};
ValueError.prototype.__repr__ = function __repr__ () {
    return "<" + __name__ + "." + "ValueError" + " #" + this._$rapyd$_object_id + ">";
};
ValueError.prototype.__str__ = function __str__ () {
    return this.__repr__();
};
ValueError.prototype.name = "ValueError";
;
    var _$rapyd$_chain_assign_temp;
function _$rapyd$_equals(a, b) {
    var _$rapyd$_unpack, akeys, bkeys, key;
    if (a === b) {
        return true;
    }
    if (a && typeof a.__eq__ === "function") {
        return a.__eq__(b);
    }
    if (b && typeof b.__eq__ === "function") {
        return b.__eq__(a);
    }
    if (_$rapyd$_arraylike(a) && _$rapyd$_arraylike(b)) {
        if ((a.length !== b.length && (typeof a.length !== "object" || _$rapyd$_not_equals(a.length, b.length)))) {
            return false;
        }
        for (var i=0; i < a.length; i++) {
            if (!((a[i] === b[i] || typeof a[i] === "object" && _$rapyd$_equals(a[i], b[i])))) {
                return false;
            }
        }
        return true;
    }
    if (a && b && a.constructor === b.constructor && a.constructor === Object) {
        _$rapyd$_unpack = [Object.keys(a), Object.keys(b)];
        akeys = _$rapyd$_unpack[0];
        bkeys = _$rapyd$_unpack[1];
        if (akeys.length !== bkeys.length) {
            return false;
        }
        for (var i=0; i < akeys.length; i++) {
            key = akeys[i];
            if (!((a[key] === b[key] || typeof a[key] === "object" && _$rapyd$_equals(a[key], b[key])))) {
                return false;
            }
        }
        return true;
    }
    return false;
}
function _$rapyd$_not_equals(a, b) {
    if (a === b) {
        return false;
    }
    if (a && typeof a.__ne__ === "function") {
        return a.__ne__(b);
    }
    if (b && typeof b.__ne__ === "function") {
        return b.__ne__(a);
    }
    return !_$rapyd$_equals(a, b);
}
var equals = _$rapyd$_equals;;
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
        if ((this[i] === val || typeof this[i] === "object" && _$rapyd$_equals(this[i], val))) {
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
    var key = (arguments[0] === undefined || ( 0 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [_$rapyd$_kwargs_symbol] === true)) ? (null) : arguments[0];
    var reverse = (arguments[1] === undefined || ( 1 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [_$rapyd$_kwargs_symbol] === true)) ? (false) : arguments[1];
    var _$rapyd$_kwargs_obj = arguments[arguments.length-1];
    if (_$rapyd$_kwargs_obj === null || typeof _$rapyd$_kwargs_obj !== "object" || _$rapyd$_kwargs_obj [_$rapyd$_kwargs_symbol] !== true) _$rapyd$_kwargs_obj = {};
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
    for (var i = 0; i < this.length; i++) {
        if ((this[i] === val || typeof this[i] === "object" && _$rapyd$_equals(this[i], val))) {
            return true;
        }
    }
    return false;
}
function _$rapyd$_list_eq(other) {
    if (!_$rapyd$_arraylike(other)) {
        return false;
    }
    if ((this.length !== other.length && (typeof this.length !== "object" || _$rapyd$_not_equals(this.length, other.length)))) {
        return false;
    }
    for (var i = 0; i < this.length; i++) {
        if (!((this[i] === other[i] || typeof this[i] === "object" && _$rapyd$_equals(this[i], other[i])))) {
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
    } else if (_$rapyd$_arraylike(iterable)) {
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
function sorted() {
    var iterable = ( 0 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [_$rapyd$_kwargs_symbol] === true) ? undefined : arguments[0];
    var key = (arguments[1] === undefined || ( 1 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [_$rapyd$_kwargs_symbol] === true)) ? (null) : arguments[1];
    var reverse = (arguments[2] === undefined || ( 2 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [_$rapyd$_kwargs_symbol] === true)) ? (false) : arguments[2];
    var _$rapyd$_kwargs_obj = arguments[arguments.length-1];
    if (_$rapyd$_kwargs_obj === null || typeof _$rapyd$_kwargs_obj !== "object" || _$rapyd$_kwargs_obj [_$rapyd$_kwargs_symbol] !== true) _$rapyd$_kwargs_obj = {};
    if (Object.prototype.hasOwnProperty.call(_$rapyd$_kwargs_obj, "key")){
        key = _$rapyd$_kwargs_obj.key;
    }
    if (Object.prototype.hasOwnProperty.call(_$rapyd$_kwargs_obj, "reverse")){
        reverse = _$rapyd$_kwargs_obj.reverse;
    }
    var ans;
    ans = _$rapyd$_list_constructor(iterable);
    ans.pysort(key, reverse);
    return ans;
}
var _$rapyd$_global_object_id = 0, _$rapyd$_set_implementation;
function _$rapyd$_set_keyfor(x) {
    var t, ans;
    t = typeof x;
    if (t === "string" || t === "number" || t === "boolean") {
        return "_" + t[0] + x;
    }
    if (x === null) {
        return "__!@#$0";
    }
    ans = x._$rapyd$_hash_key_prop;
    if (ans === undefined) {
        ans = "_!@#$" + (++_$rapyd$_global_object_id);
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
        if (_$rapyd$_arraylike(iterable)) {
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
_$rapyd$_chain_assign_temp = function(x) {
    return this.jsset.has(x);
};
_$rapyd$_set.prototype.has = _$rapyd$_chain_assign_temp;
_$rapyd$_set.prototype.__contains__ = _$rapyd$_chain_assign_temp;
;
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
_$rapyd$_chain_assign_temp = function() {
    return "{" + list(this).join(", ") + "}";
};
_$rapyd$_set.prototype.toString = _$rapyd$_chain_assign_temp;
_$rapyd$_set.prototype.inspect = _$rapyd$_chain_assign_temp;
;
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
_$rapyd$_chain_assign_temp = function(x) {
    return this.jsmap.has(x);
};
_$rapyd$_dict.prototype.has = _$rapyd$_chain_assign_temp;
_$rapyd$_dict.prototype.__contains__ = _$rapyd$_chain_assign_temp;
;
_$rapyd$_chain_assign_temp = function(key, value) {
    this.jsmap.set(key, value);
};
_$rapyd$_dict.prototype.set = _$rapyd$_chain_assign_temp;
_$rapyd$_dict.prototype.__setitem__ = _$rapyd$_chain_assign_temp;
;
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
_$rapyd$_chain_assign_temp = function() {
    return this.jsmap.entries();
};
_$rapyd$_dict.prototype.items = _$rapyd$_chain_assign_temp;
_$rapyd$_dict.prototype.entries = _$rapyd$_chain_assign_temp;
;
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
_$rapyd$_chain_assign_temp = function() {
    var iterable = ( 0 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [_$rapyd$_kwargs_symbol] === true) ? undefined : arguments[0];
    var value = (arguments[1] === undefined || ( 1 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [_$rapyd$_kwargs_symbol] === true)) ? (null) : arguments[1];
    var _$rapyd$_kwargs_obj = arguments[arguments.length-1];
    if (_$rapyd$_kwargs_obj === null || typeof _$rapyd$_kwargs_obj !== "object" || _$rapyd$_kwargs_obj [_$rapyd$_kwargs_symbol] !== true) _$rapyd$_kwargs_obj = {};
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
_$rapyd$_dict.fromkeys = _$rapyd$_chain_assign_temp;
_$rapyd$_dict.prototype.fromkeys = _$rapyd$_chain_assign_temp;
;
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
_$rapyd$_chain_assign_temp = function() {
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
_$rapyd$_dict.prototype.toString = _$rapyd$_chain_assign_temp;
_$rapyd$_dict.prototype.inspect = _$rapyd$_chain_assign_temp;
;
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
var dict = _$rapyd$_dict, dict_wrap = _$rapyd$_dict_wrap;;
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
    var parts;
    if (typeof console === "object") {
        parts = [];
        for (var i = 0; i < arguments.length; i++) {
            parts.push(_$rapyd$_str(arguments[i]));
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
function _$rapyd$_arraylike_creator() {
    var names;
    names = "Int8Array Uint8Array Uint8ClampedArray Int16Array Uint16Array Int32Array Uint32Array Float32Array Float64Array".split(" ");
    if (typeof HTMLCollection === "function") {
        names = names.concat("HTMLCollection NodeList NamedNodeMap".split(" "));
    }
    return function(x) {
        if (Array.isArray(x) || typeof x === "string" || names.indexOf(Object.prototype.toString.call(x).slice(8, -1)) > -1) {
            return true;
        }
        return false;
    };
}
function options_object(f) {
    return function() {
        if (typeof arguments[arguments.length - 1] === "object") {
            arguments[arguments.length - 1][_$rapyd$_kwargs_symbol] = true;
        }
        return f.apply(this, arguments);
    };
}
function _$rapyd$_id(x) {
    return x._$rapyd$_object_id;
}
var bool = _$rapyd$_bool, bind = _$rapyd$_bind, rebind_all = _$rapyd$_rebind_all;
var float = _$rapyd$_float, int = _$rapyd$_int, arraylike = _$rapyd$_arraylike_creator(), _$rapyd$_arraylike = arraylike;
var mixin = _$rapyd$_mixin, print = _$rapyd$_print, eslice = _$rapyd$_eslice, id = _$rapyd$_id;;
    function _$rapyd$_repr_js_builtin(x, as_array) {
    var ans, b, keys, key;
    ans = [];
    b = "{}";
    if (as_array) {
        b = "[]";
        for (var i = 0; i < x.length; i++) {
            ans.push(_$rapyd$_repr(x[i]));
        }
    } else {
        keys = Object.keys(x);
        for (var k = 0; k < keys.length; k++) {
            key = keys[k];
            ans.push(JSON.stringify(key) + ":" + _$rapyd$_repr(x[key]));
        }
    }
    return b[0] + ans.join(", ") + b[1];
}
function _$rapyd$_repr(x) {
    var ans, name;
    if (x === null) {
        return "None";
    }
    if (x === undefined) {
        return "undefined";
    }
    ans = x;
    if (typeof x.__repr__ === "function") {
        ans = x.__repr__();
    } else if (x === true || x === false) {
        ans = (x) ? "True" : "False";
    } else if (Array.isArray(x)) {
        ans = _$rapyd$_repr_js_builtin(x, true);
    } else if (typeof x === "function") {
        ans = x.toString();
    } else {
        name = Object.prototype.toString.call(x).slice(8, -1);
        if (_$rapyd$_not_equals("Int8Array Uint8Array Uint8ClampedArray Int16Array Uint16Array Int32Array Uint32Array Float32Array Float64Array".indexOf(name), -1)) {
            return name + "([" + x.map(function(i) {
                return str.format("0x{:02x}", i);
            }).join(", ") + "])";
        }
        ans = (typeof x.toString === "function") ? x.toString() : x;
        if (ans === "[object Object]") {
            return _$rapyd$_repr_js_builtin(x);
        }
        try {
            ans = JSON.stringify(x);
        } catch (_$rapyd$_Exception) {
        }
    }
    return ans + "";
}
function _$rapyd$_str(x) {
    var ans, name;
    if (x === null) {
        return "None";
    }
    if (x === undefined) {
        return "undefined";
    }
    ans = x;
    if (typeof x.__str__ === "function") {
        ans = x.__str__();
    } else if (typeof x.__repr__ === "function") {
        ans = x.__repr__();
    } else if (x === true || x === false) {
        ans = (x) ? "True" : "False";
    } else if (Array.isArray(x)) {
        ans = _$rapyd$_repr_js_builtin(x, true);
    } else if (typeof x.toString === "function") {
        name = Object.prototype.toString.call(x).slice(8, -1);
        if (_$rapyd$_not_equals("Int8Array Uint8Array Uint8ClampedArray Int16Array Uint16Array Int32Array Uint32Array Float32Array Float64Array".indexOf(name), -1)) {
            return name + "([" + x.map(function(i) {
                return str.format("0x{:02x}", i);
            }).join(", ") + "])";
        }
        ans = x.toString();
        if (ans === "[object Object]") {
            ans = _$rapyd$_repr_js_builtin(x);
        }
    }
    return ans + "";
}
_$rapyd$_str.format = function() {
    var template, args, kwargs, explicit, implicit, _$rapyd$_chain_assign_temp, idx, ans, pos, in_brace, markup, ch;
    template = arguments[0];
    if (template === undefined) {
        throw new TypeError("Template is required");
    }
    args = Array.prototype.slice.call(arguments, 1);
    kwargs = {};
    if (args.length && args[args.length-1][_$rapyd$_kwargs_symbol] !== undefined) {
        kwargs = args[args.length-1];
        args = args.slice(0, -1);
    }
    _$rapyd$_chain_assign_temp = false;
    explicit = _$rapyd$_chain_assign_temp;
    implicit = _$rapyd$_chain_assign_temp;
;
    idx = 0;
    if (_$rapyd$_str.format._template_resolve_pat === undefined) {
        _$rapyd$_str.format._template_resolve_pat = /[.\[]/;
    }
    function resolve(arg, object) {
        var _$rapyd$_unpack, first, key, rest, ans;
        if (!arg) {
            return object;
        }
        _$rapyd$_unpack = [arg[0], arg.slice(1)];
        first = _$rapyd$_unpack[0];
        arg = _$rapyd$_unpack[1];
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
        var _$rapyd$_unpack, fill, align, sign, fhash, zeropad, width, comma, precision, ftype, is_numeric, is_int, lftype, code, exp, nval, is_positive, left, right;
        if (format_spec.indexOf("{") !== -1) {
            format_spec = resolve_format_spec(format_spec);
        }
        if (_$rapyd$_str.format._template_format_pat === undefined) {
            _$rapyd$_str.format._template_format_pat = /([^{}](?=[<>=^]))?([<>=^])?([-+\x20])?(\#)?(0)?(\d+)?(,)?(?:\.(\d+))?([bcdeEfFgGnosxX%])?/;
        }
        try {
            _$rapyd$_unpack = format_spec.match(_$rapyd$_str.format._template_format_pat).slice(1);
            fill = _$rapyd$_unpack[0];
            align = _$rapyd$_unpack[1];
            sign = _$rapyd$_unpack[2];
            fhash = _$rapyd$_unpack[3];
            zeropad = _$rapyd$_unpack[4];
            width = _$rapyd$_unpack[5];
            comma = _$rapyd$_unpack[6];
            precision = _$rapyd$_unpack[7];
            ftype = _$rapyd$_unpack[8];
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
            nval = Number(value);
            is_positive = !isNaN(nval) && nval >= 0;
            if (is_positive && (sign === " " || sign === "+")) {
                value = sign + value;
            }
        }
        function repeat(char, num) {
            return (new Array(num+1)).join(char);
        }
        if (is_numeric && width && width[0] === "0") {
            width = width.slice(1);
            _$rapyd$_unpack = ["0", "="];
            fill = _$rapyd$_unpack[0];
            align = _$rapyd$_unpack[1];
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
        var key, transformer, format_spec, _$rapyd$_chain_assign_temp, pos, state, ch;
        _$rapyd$_chain_assign_temp = "";
        key = _$rapyd$_chain_assign_temp;
        transformer = _$rapyd$_chain_assign_temp;
        format_spec = _$rapyd$_chain_assign_temp;
;
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
        var _$rapyd$_unpack, key, transformer, format_spec, lkey, nvalue, object, ans;
        _$rapyd$_unpack = parse_markup(markup);
        key = _$rapyd$_unpack[0];
        transformer = _$rapyd$_unpack[1];
        format_spec = _$rapyd$_unpack[2];
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
    return new Array(left+1).join(fill) + string + new Array(right+1).join(fill);
};
_$rapyd$_str.count = function(string, needle, start, end) {
    var _$rapyd$_unpack, pos, step, ans;
    start = start || 0;
    end = end || string.length;
    if (start < 0 || end < 0) {
        string = string.slice(start, end);
        _$rapyd$_unpack = [0, string.length];
        start = _$rapyd$_unpack[0];
        end = _$rapyd$_unpack[1];
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
        string += new Array(width - string.length + 1).join(fill);
    }
    return string;
};
_$rapyd$_str.rjust = function(string, width, fill) {
    if (width > string.length) {
        fill = fill || " ";
        string = new Array(width - string.length + 1).join(fill) + string;
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
    var ans, is_space, pos, current, spc, ch, end, _$rapyd$_chain_assign_temp, idx;
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
        _$rapyd$_chain_assign_temp = string.length;
        pos = _$rapyd$_chain_assign_temp;
        end = _$rapyd$_chain_assign_temp;
;
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
    ans = new Array(string.length);
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
        string = new Array(width - string.length + 1).join("0") + string;
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
var str = _$rapyd$_str, repr = _$rapyd$_repr;;
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
            if (_$rapyd$_arraylike(iterable)) {
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
        };
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
        };
    var _$rapyd$_modules = {};
    _$rapyd$_modules["aes"] = {};
    _$rapyd$_modules["crypto"] = {};
    _$rapyd$_modules["qt"] = {};
    _$rapyd$_modules["frames"] = {};
    _$rapyd$_modules["middle_click"] = {};
    _$rapyd$_modules["focus"] = {};
    _$rapyd$_modules["elementmaker"] = {};
    _$rapyd$_modules["humanize"] = {};
    _$rapyd$_modules["downloads"] = {};
    _$rapyd$_modules["utils"] = {};
    _$rapyd$_modules["links"] = {};
    _$rapyd$_modules["follow_next"] = {};
    _$rapyd$_modules["passwd"] = {};

    (function(){
        var __name__ = "aes";
        var string_to_bytes, bytes_to_string, _$rapyd$_chain_assign_temp, number_of_rounds, rcon, S, Si, T1, T2, T3, T4, T5, T6, T7, T8, U1, U2, U3, U4, random_bytes, noderandom;
        function string_to_bytes_encoder(string) {
            return new TextEncoder("utf-8").encode(string + "");
        }
        function string_to_bytes_slow(string) {
            var escstr, binstr, ua;
            escstr = encodeURIComponent(string);
            binstr = escstr.replace(/%([0-9A-F]{2})/g, function(match, p1) {
                return String.fromCharCode("0x" + p1);
            });
            ua = new Uint8Array(binstr.length);
            Array.prototype.forEach.call(binstr, function(ch, i) {
                ua[i] = ch.charCodeAt(0);
            });
            return ua;
        }
        function as_hex() {
            var array = ( 0 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [_$rapyd$_kwargs_symbol] === true) ? undefined : arguments[0];
            var sep = (arguments[1] === undefined || ( 1 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [_$rapyd$_kwargs_symbol] === true)) ? ("") : arguments[1];
            var _$rapyd$_kwargs_obj = arguments[arguments.length-1];
            if (_$rapyd$_kwargs_obj === null || typeof _$rapyd$_kwargs_obj !== "object" || _$rapyd$_kwargs_obj [_$rapyd$_kwargs_symbol] !== true) _$rapyd$_kwargs_obj = {};
            if (Object.prototype.hasOwnProperty.call(_$rapyd$_kwargs_obj, "sep")){
                sep = _$rapyd$_kwargs_obj.sep;
            }
            var num, fmt;
            num = array.BYTES_PER_ELEMENT || 1;
            fmt = "{:0" + num * 2 + "x}";
            return (function() {
                var _$rapyd$_Iter = _$rapyd$_Iterable(array), _$rapyd$_Result = [], x;
                for (var _$rapyd$_Index = 0; _$rapyd$_Index < _$rapyd$_Iter.length; _$rapyd$_Index++) {
                    x = _$rapyd$_Iter[_$rapyd$_Index];
                    _$rapyd$_Result.push(str.format(fmt, x));
                }
                _$rapyd$_Result = _$rapyd$_list_constructor(_$rapyd$_Result);
                return _$rapyd$_Result;
            })().join(sep);
        }
        function bytes_to_string_decoder(bytes, offset) {
            offset = offset || 0;
            if (offset) {
                bytes = bytes.subarray(offset);
            }
            return new TextDecoder("utf-8").decode(bytes);
        }
        function bytes_to_string_slow(bytes, offset) {
            var ans, i, c;
            ans = [];
            i = offset || 0;
            while (i < bytes.length) {
                c = bytes[i];
                if (c < 128) {
                    ans.push(String.fromCharCode(c));
                    i += 1;
                } else if (191 < c && c < 224) {
                    ans.push(String.fromCharCode((c & 31) << 6 | bytes[i + 1] & 63));
                    i += 2;
                } else {
                    ans.push(String.fromCharCode((c & 15) << 12 | (bytes[i + 1] & 63) << 6 | bytes[i + 2] & 63));
                    i += 3;
                }
            }
            return ans.join("");
        }
        string_to_bytes = (typeof TextEncoder === "function") ? string_to_bytes_encoder : string_to_bytes_slow;
        bytes_to_string = (typeof TextDecoder === "function") ? bytes_to_string_decoder : bytes_to_string_slow;
        function increment_counter(c) {
            for (var i = 15; i >= 12; i--) {
                if (c[i] === 255) {
                    c[i] = 0;
                } else {
                    c[i] += 1;
                    break;
                }
            }
        }
        function convert_to_int32(bytes, output, offset, length) {
            offset = offset || 0;
            length = length || bytes.length;
            for (var i = offset, j = 0; i < offset + length; i += 4, j++) {
                output[j] = bytes[i] << 24 | bytes[i + 1] << 16 | bytes[i + 2] << 8 | bytes[i + 3];
            }
        }
        function convert_to_int32_pad(bytes) {
            var extra, t, ans;
            extra = bytes.length % 4;
            if (extra) {
                t = new Uint8Array(bytes.length + 4 - extra);
                t.set(bytes);
                bytes = t;
            }
            ans = new Uint32Array(bytes.length / 4);
            convert_to_int32(bytes, ans);
            return ans;
        }
        if (!Uint8Array.prototype.fill) {
            _$rapyd$_chain_assign_temp = function(val) {
                for (var i = 0; i < this.length; i++) {
                    this[i] = val;
                }
            };
            Uint8Array.prototype.fill = _$rapyd$_chain_assign_temp;
            Uint32Array.prototype.fill = _$rapyd$_chain_assign_temp;
;
        }
        function from_64_to_32(num) {
            var ans;
            ans = new Uint32Array(2);
            ans[0] = num / 4294967296 | 0;
            ans[1] = num & 4294967295;
            return ans;
        }
        number_of_rounds = {
            16: 10,
            24: 12,
            32: 14
        };
        rcon = new Uint32Array([0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91]);
        S = new Uint32Array([0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76, 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15, 0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84, 0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8, 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73, 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79, 0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08, 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e, 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]);
        Si = new Uint32Array([0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb, 0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb, 0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e, 0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25, 0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92, 0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84, 0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06, 0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b, 0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73, 0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e, 0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b, 0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4, 0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f, 0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef, 0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61, 0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]);
        T1 = new Uint32Array([0xc66363a5, 0xf87c7c84, 0xee777799, 0xf67b7b8d, 0xfff2f20d, 0xd66b6bbd, 0xde6f6fb1, 0x91c5c554, 0x60303050, 0x02010103, 0xce6767a9, 0x562b2b7d, 0xe7fefe19, 0xb5d7d762, 0x4dababe6, 0xec76769a, 0x8fcaca45, 0x1f82829d, 0x89c9c940, 0xfa7d7d87, 0xeffafa15, 0xb25959eb, 0x8e4747c9, 0xfbf0f00b, 0x41adadec, 0xb3d4d467, 0x5fa2a2fd, 0x45afafea, 0x239c9cbf, 0x53a4a4f7, 0xe4727296, 0x9bc0c05b, 0x75b7b7c2, 0xe1fdfd1c, 0x3d9393ae, 0x4c26266a, 0x6c36365a, 0x7e3f3f41, 0xf5f7f702, 0x83cccc4f, 0x6834345c, 0x51a5a5f4, 0xd1e5e534, 0xf9f1f108, 0xe2717193, 0xabd8d873, 0x62313153, 0x2a15153f, 0x0804040c, 0x95c7c752, 0x46232365, 0x9dc3c35e, 0x30181828, 0x379696a1, 0x0a05050f, 0x2f9a9ab5, 0x0e070709, 0x24121236, 0x1b80809b, 0xdfe2e23d, 0xcdebeb26, 0x4e272769, 0x7fb2b2cd, 0xea75759f, 0x1209091b, 0x1d83839e, 0x582c2c74, 0x341a1a2e, 0x361b1b2d, 0xdc6e6eb2, 0xb45a5aee, 0x5ba0a0fb, 0xa45252f6, 0x763b3b4d, 0xb7d6d661, 0x7db3b3ce, 0x5229297b, 0xdde3e33e, 0x5e2f2f71, 0x13848497, 0xa65353f5, 0xb9d1d168, 0x00000000, 0xc1eded2c, 0x40202060, 0xe3fcfc1f, 0x79b1b1c8, 0xb65b5bed, 0xd46a6abe, 0x8dcbcb46, 0x67bebed9, 0x7239394b, 0x944a4ade, 0x984c4cd4, 0xb05858e8, 0x85cfcf4a, 0xbbd0d06b, 0xc5efef2a, 0x4faaaae5, 0xedfbfb16, 0x864343c5, 0x9a4d4dd7, 0x66333355, 0x11858594, 0x8a4545cf, 0xe9f9f910, 0x04020206, 0xfe7f7f81, 0xa05050f0, 0x783c3c44, 0x259f9fba, 0x4ba8a8e3, 0xa25151f3, 0x5da3a3fe, 0x804040c0, 0x058f8f8a, 0x3f9292ad, 0x219d9dbc, 0x70383848, 0xf1f5f504, 0x63bcbcdf, 0x77b6b6c1, 0xafdada75, 0x42212163, 0x20101030, 0xe5ffff1a, 0xfdf3f30e, 0xbfd2d26d, 0x81cdcd4c, 0x180c0c14, 0x26131335, 0xc3ecec2f, 0xbe5f5fe1, 0x359797a2, 0x884444cc, 0x2e171739, 0x93c4c457, 0x55a7a7f2, 0xfc7e7e82, 0x7a3d3d47, 0xc86464ac, 0xba5d5de7, 0x3219192b, 0xe6737395, 0xc06060a0, 0x19818198, 0x9e4f4fd1, 0xa3dcdc7f, 0x44222266, 0x542a2a7e, 0x3b9090ab, 0x0b888883, 0x8c4646ca, 0xc7eeee29, 0x6bb8b8d3, 0x2814143c, 0xa7dede79, 0xbc5e5ee2, 0x160b0b1d, 0xaddbdb76, 0xdbe0e03b, 0x64323256, 0x743a3a4e, 0x140a0a1e, 0x924949db, 0x0c06060a, 0x4824246c, 0xb85c5ce4, 0x9fc2c25d, 0xbdd3d36e, 0x43acacef, 0xc46262a6, 0x399191a8, 0x319595a4, 0xd3e4e437, 0xf279798b, 0xd5e7e732, 0x8bc8c843, 0x6e373759, 0xda6d6db7, 0x018d8d8c, 0xb1d5d564, 0x9c4e4ed2, 0x49a9a9e0, 0xd86c6cb4, 0xac5656fa, 0xf3f4f407, 0xcfeaea25, 0xca6565af, 0xf47a7a8e, 0x47aeaee9, 0x10080818, 0x6fbabad5, 0xf0787888, 0x4a25256f, 0x5c2e2e72, 0x381c1c24, 0x57a6a6f1, 0x73b4b4c7, 0x97c6c651, 0xcbe8e823, 0xa1dddd7c, 0xe874749c, 0x3e1f1f21, 0x964b4bdd, 0x61bdbddc, 0x0d8b8b86, 0x0f8a8a85, 0xe0707090, 0x7c3e3e42, 0x71b5b5c4, 0xcc6666aa, 0x904848d8, 0x06030305, 0xf7f6f601, 0x1c0e0e12, 0xc26161a3, 0x6a35355f, 0xae5757f9, 0x69b9b9d0, 0x17868691, 0x99c1c158, 0x3a1d1d27, 0x279e9eb9, 0xd9e1e138, 0xebf8f813, 0x2b9898b3, 0x22111133, 0xd26969bb, 0xa9d9d970, 0x078e8e89, 0x339494a7, 0x2d9b9bb6, 0x3c1e1e22, 0x15878792, 0xc9e9e920, 0x87cece49, 0xaa5555ff, 0x50282878, 0xa5dfdf7a, 0x038c8c8f, 0x59a1a1f8, 0x09898980, 0x1a0d0d17, 0x65bfbfda, 0xd7e6e631, 0x844242c6, 0xd06868b8, 0x824141c3, 0x299999b0, 0x5a2d2d77, 0x1e0f0f11, 0x7bb0b0cb, 0xa85454fc, 0x6dbbbbd6, 0x2c16163a]);
        T2 = new Uint32Array([0xa5c66363, 0x84f87c7c, 0x99ee7777, 0x8df67b7b, 0x0dfff2f2, 0xbdd66b6b, 0xb1de6f6f, 0x5491c5c5, 0x50603030, 0x03020101, 0xa9ce6767, 0x7d562b2b, 0x19e7fefe, 0x62b5d7d7, 0xe64dabab, 0x9aec7676, 0x458fcaca, 0x9d1f8282, 0x4089c9c9, 0x87fa7d7d, 0x15effafa, 0xebb25959, 0xc98e4747, 0x0bfbf0f0, 0xec41adad, 0x67b3d4d4, 0xfd5fa2a2, 0xea45afaf, 0xbf239c9c, 0xf753a4a4, 0x96e47272, 0x5b9bc0c0, 0xc275b7b7, 0x1ce1fdfd, 0xae3d9393, 0x6a4c2626, 0x5a6c3636, 0x417e3f3f, 0x02f5f7f7, 0x4f83cccc, 0x5c683434, 0xf451a5a5, 0x34d1e5e5, 0x08f9f1f1, 0x93e27171, 0x73abd8d8, 0x53623131, 0x3f2a1515, 0x0c080404, 0x5295c7c7, 0x65462323, 0x5e9dc3c3, 0x28301818, 0xa1379696, 0x0f0a0505, 0xb52f9a9a, 0x090e0707, 0x36241212, 0x9b1b8080, 0x3ddfe2e2, 0x26cdebeb, 0x694e2727, 0xcd7fb2b2, 0x9fea7575, 0x1b120909, 0x9e1d8383, 0x74582c2c, 0x2e341a1a, 0x2d361b1b, 0xb2dc6e6e, 0xeeb45a5a, 0xfb5ba0a0, 0xf6a45252, 0x4d763b3b, 0x61b7d6d6, 0xce7db3b3, 0x7b522929, 0x3edde3e3, 0x715e2f2f, 0x97138484, 0xf5a65353, 0x68b9d1d1, 0x00000000, 0x2cc1eded, 0x60402020, 0x1fe3fcfc, 0xc879b1b1, 0xedb65b5b, 0xbed46a6a, 0x468dcbcb, 0xd967bebe, 0x4b723939, 0xde944a4a, 0xd4984c4c, 0xe8b05858, 0x4a85cfcf, 0x6bbbd0d0, 0x2ac5efef, 0xe54faaaa, 0x16edfbfb, 0xc5864343, 0xd79a4d4d, 0x55663333, 0x94118585, 0xcf8a4545, 0x10e9f9f9, 0x06040202, 0x81fe7f7f, 0xf0a05050, 0x44783c3c, 0xba259f9f, 0xe34ba8a8, 0xf3a25151, 0xfe5da3a3, 0xc0804040, 0x8a058f8f, 0xad3f9292, 0xbc219d9d, 0x48703838, 0x04f1f5f5, 0xdf63bcbc, 0xc177b6b6, 0x75afdada, 0x63422121, 0x30201010, 0x1ae5ffff, 0x0efdf3f3, 0x6dbfd2d2, 0x4c81cdcd, 0x14180c0c, 0x35261313, 0x2fc3ecec, 0xe1be5f5f, 0xa2359797, 0xcc884444, 0x392e1717, 0x5793c4c4, 0xf255a7a7, 0x82fc7e7e, 0x477a3d3d, 0xacc86464, 0xe7ba5d5d, 0x2b321919, 0x95e67373, 0xa0c06060, 0x98198181, 0xd19e4f4f, 0x7fa3dcdc, 0x66442222, 0x7e542a2a, 0xab3b9090, 0x830b8888, 0xca8c4646, 0x29c7eeee, 0xd36bb8b8, 0x3c281414, 0x79a7dede, 0xe2bc5e5e, 0x1d160b0b, 0x76addbdb, 0x3bdbe0e0, 0x56643232, 0x4e743a3a, 0x1e140a0a, 0xdb924949, 0x0a0c0606, 0x6c482424, 0xe4b85c5c, 0x5d9fc2c2, 0x6ebdd3d3, 0xef43acac, 0xa6c46262, 0xa8399191, 0xa4319595, 0x37d3e4e4, 0x8bf27979, 0x32d5e7e7, 0x438bc8c8, 0x596e3737, 0xb7da6d6d, 0x8c018d8d, 0x64b1d5d5, 0xd29c4e4e, 0xe049a9a9, 0xb4d86c6c, 0xfaac5656, 0x07f3f4f4, 0x25cfeaea, 0xafca6565, 0x8ef47a7a, 0xe947aeae, 0x18100808, 0xd56fbaba, 0x88f07878, 0x6f4a2525, 0x725c2e2e, 0x24381c1c, 0xf157a6a6, 0xc773b4b4, 0x5197c6c6, 0x23cbe8e8, 0x7ca1dddd, 0x9ce87474, 0x213e1f1f, 0xdd964b4b, 0xdc61bdbd, 0x860d8b8b, 0x850f8a8a, 0x90e07070, 0x427c3e3e, 0xc471b5b5, 0xaacc6666, 0xd8904848, 0x05060303, 0x01f7f6f6, 0x121c0e0e, 0xa3c26161, 0x5f6a3535, 0xf9ae5757, 0xd069b9b9, 0x91178686, 0x5899c1c1, 0x273a1d1d, 0xb9279e9e, 0x38d9e1e1, 0x13ebf8f8, 0xb32b9898, 0x33221111, 0xbbd26969, 0x70a9d9d9, 0x89078e8e, 0xa7339494, 0xb62d9b9b, 0x223c1e1e, 0x92158787, 0x20c9e9e9, 0x4987cece, 0xffaa5555, 0x78502828, 0x7aa5dfdf, 0x8f038c8c, 0xf859a1a1, 0x80098989, 0x171a0d0d, 0xda65bfbf, 0x31d7e6e6, 0xc6844242, 0xb8d06868, 0xc3824141, 0xb0299999, 0x775a2d2d, 0x111e0f0f, 0xcb7bb0b0, 0xfca85454, 0xd66dbbbb, 0x3a2c1616]);
        T3 = new Uint32Array([0x63a5c663, 0x7c84f87c, 0x7799ee77, 0x7b8df67b, 0xf20dfff2, 0x6bbdd66b, 0x6fb1de6f, 0xc55491c5, 0x30506030, 0x01030201, 0x67a9ce67, 0x2b7d562b, 0xfe19e7fe, 0xd762b5d7, 0xabe64dab, 0x769aec76, 0xca458fca, 0x829d1f82, 0xc94089c9, 0x7d87fa7d, 0xfa15effa, 0x59ebb259, 0x47c98e47, 0xf00bfbf0, 0xadec41ad, 0xd467b3d4, 0xa2fd5fa2, 0xafea45af, 0x9cbf239c, 0xa4f753a4, 0x7296e472, 0xc05b9bc0, 0xb7c275b7, 0xfd1ce1fd, 0x93ae3d93, 0x266a4c26, 0x365a6c36, 0x3f417e3f, 0xf702f5f7, 0xcc4f83cc, 0x345c6834, 0xa5f451a5, 0xe534d1e5, 0xf108f9f1, 0x7193e271, 0xd873abd8, 0x31536231, 0x153f2a15, 0x040c0804, 0xc75295c7, 0x23654623, 0xc35e9dc3, 0x18283018, 0x96a13796, 0x050f0a05, 0x9ab52f9a, 0x07090e07, 0x12362412, 0x809b1b80, 0xe23ddfe2, 0xeb26cdeb, 0x27694e27, 0xb2cd7fb2, 0x759fea75, 0x091b1209, 0x839e1d83, 0x2c74582c, 0x1a2e341a, 0x1b2d361b, 0x6eb2dc6e, 0x5aeeb45a, 0xa0fb5ba0, 0x52f6a452, 0x3b4d763b, 0xd661b7d6, 0xb3ce7db3, 0x297b5229, 0xe33edde3, 0x2f715e2f, 0x84971384, 0x53f5a653, 0xd168b9d1, 0x00000000, 0xed2cc1ed, 0x20604020, 0xfc1fe3fc, 0xb1c879b1, 0x5bedb65b, 0x6abed46a, 0xcb468dcb, 0xbed967be, 0x394b7239, 0x4ade944a, 0x4cd4984c, 0x58e8b058, 0xcf4a85cf, 0xd06bbbd0, 0xef2ac5ef, 0xaae54faa, 0xfb16edfb, 0x43c58643, 0x4dd79a4d, 0x33556633, 0x85941185, 0x45cf8a45, 0xf910e9f9, 0x02060402, 0x7f81fe7f, 0x50f0a050, 0x3c44783c, 0x9fba259f, 0xa8e34ba8, 0x51f3a251, 0xa3fe5da3, 0x40c08040, 0x8f8a058f, 0x92ad3f92, 0x9dbc219d, 0x38487038, 0xf504f1f5, 0xbcdf63bc, 0xb6c177b6, 0xda75afda, 0x21634221, 0x10302010, 0xff1ae5ff, 0xf30efdf3, 0xd26dbfd2, 0xcd4c81cd, 0x0c14180c, 0x13352613, 0xec2fc3ec, 0x5fe1be5f, 0x97a23597, 0x44cc8844, 0x17392e17, 0xc45793c4, 0xa7f255a7, 0x7e82fc7e, 0x3d477a3d, 0x64acc864, 0x5de7ba5d, 0x192b3219, 0x7395e673, 0x60a0c060, 0x81981981, 0x4fd19e4f, 0xdc7fa3dc, 0x22664422, 0x2a7e542a, 0x90ab3b90, 0x88830b88, 0x46ca8c46, 0xee29c7ee, 0xb8d36bb8, 0x143c2814, 0xde79a7de, 0x5ee2bc5e, 0x0b1d160b, 0xdb76addb, 0xe03bdbe0, 0x32566432, 0x3a4e743a, 0x0a1e140a, 0x49db9249, 0x060a0c06, 0x246c4824, 0x5ce4b85c, 0xc25d9fc2, 0xd36ebdd3, 0xacef43ac, 0x62a6c462, 0x91a83991, 0x95a43195, 0xe437d3e4, 0x798bf279, 0xe732d5e7, 0xc8438bc8, 0x37596e37, 0x6db7da6d, 0x8d8c018d, 0xd564b1d5, 0x4ed29c4e, 0xa9e049a9, 0x6cb4d86c, 0x56faac56, 0xf407f3f4, 0xea25cfea, 0x65afca65, 0x7a8ef47a, 0xaee947ae, 0x08181008, 0xbad56fba, 0x7888f078, 0x256f4a25, 0x2e725c2e, 0x1c24381c, 0xa6f157a6, 0xb4c773b4, 0xc65197c6, 0xe823cbe8, 0xdd7ca1dd, 0x749ce874, 0x1f213e1f, 0x4bdd964b, 0xbddc61bd, 0x8b860d8b, 0x8a850f8a, 0x7090e070, 0x3e427c3e, 0xb5c471b5, 0x66aacc66, 0x48d89048, 0x03050603, 0xf601f7f6, 0x0e121c0e, 0x61a3c261, 0x355f6a35, 0x57f9ae57, 0xb9d069b9, 0x86911786, 0xc15899c1, 0x1d273a1d, 0x9eb9279e, 0xe138d9e1, 0xf813ebf8, 0x98b32b98, 0x11332211, 0x69bbd269, 0xd970a9d9, 0x8e89078e, 0x94a73394, 0x9bb62d9b, 0x1e223c1e, 0x87921587, 0xe920c9e9, 0xce4987ce, 0x55ffaa55, 0x28785028, 0xdf7aa5df, 0x8c8f038c, 0xa1f859a1, 0x89800989, 0x0d171a0d, 0xbfda65bf, 0xe631d7e6, 0x42c68442, 0x68b8d068, 0x41c38241, 0x99b02999, 0x2d775a2d, 0x0f111e0f, 0xb0cb7bb0, 0x54fca854, 0xbbd66dbb, 0x163a2c16]);
        T4 = new Uint32Array([0x6363a5c6, 0x7c7c84f8, 0x777799ee, 0x7b7b8df6, 0xf2f20dff, 0x6b6bbdd6, 0x6f6fb1de, 0xc5c55491, 0x30305060, 0x01010302, 0x6767a9ce, 0x2b2b7d56, 0xfefe19e7, 0xd7d762b5, 0xababe64d, 0x76769aec, 0xcaca458f, 0x82829d1f, 0xc9c94089, 0x7d7d87fa, 0xfafa15ef, 0x5959ebb2, 0x4747c98e, 0xf0f00bfb, 0xadadec41, 0xd4d467b3, 0xa2a2fd5f, 0xafafea45, 0x9c9cbf23, 0xa4a4f753, 0x727296e4, 0xc0c05b9b, 0xb7b7c275, 0xfdfd1ce1, 0x9393ae3d, 0x26266a4c, 0x36365a6c, 0x3f3f417e, 0xf7f702f5, 0xcccc4f83, 0x34345c68, 0xa5a5f451, 0xe5e534d1, 0xf1f108f9, 0x717193e2, 0xd8d873ab, 0x31315362, 0x15153f2a, 0x04040c08, 0xc7c75295, 0x23236546, 0xc3c35e9d, 0x18182830, 0x9696a137, 0x05050f0a, 0x9a9ab52f, 0x0707090e, 0x12123624, 0x80809b1b, 0xe2e23ddf, 0xebeb26cd, 0x2727694e, 0xb2b2cd7f, 0x75759fea, 0x09091b12, 0x83839e1d, 0x2c2c7458, 0x1a1a2e34, 0x1b1b2d36, 0x6e6eb2dc, 0x5a5aeeb4, 0xa0a0fb5b, 0x5252f6a4, 0x3b3b4d76, 0xd6d661b7, 0xb3b3ce7d, 0x29297b52, 0xe3e33edd, 0x2f2f715e, 0x84849713, 0x5353f5a6, 0xd1d168b9, 0x00000000, 0xeded2cc1, 0x20206040, 0xfcfc1fe3, 0xb1b1c879, 0x5b5bedb6, 0x6a6abed4, 0xcbcb468d, 0xbebed967, 0x39394b72, 0x4a4ade94, 0x4c4cd498, 0x5858e8b0, 0xcfcf4a85, 0xd0d06bbb, 0xefef2ac5, 0xaaaae54f, 0xfbfb16ed, 0x4343c586, 0x4d4dd79a, 0x33335566, 0x85859411, 0x4545cf8a, 0xf9f910e9, 0x02020604, 0x7f7f81fe, 0x5050f0a0, 0x3c3c4478, 0x9f9fba25, 0xa8a8e34b, 0x5151f3a2, 0xa3a3fe5d, 0x4040c080, 0x8f8f8a05, 0x9292ad3f, 0x9d9dbc21, 0x38384870, 0xf5f504f1, 0xbcbcdf63, 0xb6b6c177, 0xdada75af, 0x21216342, 0x10103020, 0xffff1ae5, 0xf3f30efd, 0xd2d26dbf, 0xcdcd4c81, 0x0c0c1418, 0x13133526, 0xecec2fc3, 0x5f5fe1be, 0x9797a235, 0x4444cc88, 0x1717392e, 0xc4c45793, 0xa7a7f255, 0x7e7e82fc, 0x3d3d477a, 0x6464acc8, 0x5d5de7ba, 0x19192b32, 0x737395e6, 0x6060a0c0, 0x81819819, 0x4f4fd19e, 0xdcdc7fa3, 0x22226644, 0x2a2a7e54, 0x9090ab3b, 0x8888830b, 0x4646ca8c, 0xeeee29c7, 0xb8b8d36b, 0x14143c28, 0xdede79a7, 0x5e5ee2bc, 0x0b0b1d16, 0xdbdb76ad, 0xe0e03bdb, 0x32325664, 0x3a3a4e74, 0x0a0a1e14, 0x4949db92, 0x06060a0c, 0x24246c48, 0x5c5ce4b8, 0xc2c25d9f, 0xd3d36ebd, 0xacacef43, 0x6262a6c4, 0x9191a839, 0x9595a431, 0xe4e437d3, 0x79798bf2, 0xe7e732d5, 0xc8c8438b, 0x3737596e, 0x6d6db7da, 0x8d8d8c01, 0xd5d564b1, 0x4e4ed29c, 0xa9a9e049, 0x6c6cb4d8, 0x5656faac, 0xf4f407f3, 0xeaea25cf, 0x6565afca, 0x7a7a8ef4, 0xaeaee947, 0x08081810, 0xbabad56f, 0x787888f0, 0x25256f4a, 0x2e2e725c, 0x1c1c2438, 0xa6a6f157, 0xb4b4c773, 0xc6c65197, 0xe8e823cb, 0xdddd7ca1, 0x74749ce8, 0x1f1f213e, 0x4b4bdd96, 0xbdbddc61, 0x8b8b860d, 0x8a8a850f, 0x707090e0, 0x3e3e427c, 0xb5b5c471, 0x6666aacc, 0x4848d890, 0x03030506, 0xf6f601f7, 0x0e0e121c, 0x6161a3c2, 0x35355f6a, 0x5757f9ae, 0xb9b9d069, 0x86869117, 0xc1c15899, 0x1d1d273a, 0x9e9eb927, 0xe1e138d9, 0xf8f813eb, 0x9898b32b, 0x11113322, 0x6969bbd2, 0xd9d970a9, 0x8e8e8907, 0x9494a733, 0x9b9bb62d, 0x1e1e223c, 0x87879215, 0xe9e920c9, 0xcece4987, 0x5555ffaa, 0x28287850, 0xdfdf7aa5, 0x8c8c8f03, 0xa1a1f859, 0x89898009, 0x0d0d171a, 0xbfbfda65, 0xe6e631d7, 0x4242c684, 0x6868b8d0, 0x4141c382, 0x9999b029, 0x2d2d775a, 0x0f0f111e, 0xb0b0cb7b, 0x5454fca8, 0xbbbbd66d, 0x16163a2c]);
        T5 = new Uint32Array([0x51f4a750, 0x7e416553, 0x1a17a4c3, 0x3a275e96, 0x3bab6bcb, 0x1f9d45f1, 0xacfa58ab, 0x4be30393, 0x2030fa55, 0xad766df6, 0x88cc7691, 0xf5024c25, 0x4fe5d7fc, 0xc52acbd7, 0x26354480, 0xb562a38f, 0xdeb15a49, 0x25ba1b67, 0x45ea0e98, 0x5dfec0e1, 0xc32f7502, 0x814cf012, 0x8d4697a3, 0x6bd3f9c6, 0x038f5fe7, 0x15929c95, 0xbf6d7aeb, 0x955259da, 0xd4be832d, 0x587421d3, 0x49e06929, 0x8ec9c844, 0x75c2896a, 0xf48e7978, 0x99583e6b, 0x27b971dd, 0xbee14fb6, 0xf088ad17, 0xc920ac66, 0x7dce3ab4, 0x63df4a18, 0xe51a3182, 0x97513360, 0x62537f45, 0xb16477e0, 0xbb6bae84, 0xfe81a01c, 0xf9082b94, 0x70486858, 0x8f45fd19, 0x94de6c87, 0x527bf8b7, 0xab73d323, 0x724b02e2, 0xe31f8f57, 0x6655ab2a, 0xb2eb2807, 0x2fb5c203, 0x86c57b9a, 0xd33708a5, 0x302887f2, 0x23bfa5b2, 0x02036aba, 0xed16825c, 0x8acf1c2b, 0xa779b492, 0xf307f2f0, 0x4e69e2a1, 0x65daf4cd, 0x0605bed5, 0xd134621f, 0xc4a6fe8a, 0x342e539d, 0xa2f355a0, 0x058ae132, 0xa4f6eb75, 0x0b83ec39, 0x4060efaa, 0x5e719f06, 0xbd6e1051, 0x3e218af9, 0x96dd063d, 0xdd3e05ae, 0x4de6bd46, 0x91548db5, 0x71c45d05, 0x0406d46f, 0x605015ff, 0x1998fb24, 0xd6bde997, 0x894043cc, 0x67d99e77, 0xb0e842bd, 0x07898b88, 0xe7195b38, 0x79c8eedb, 0xa17c0a47, 0x7c420fe9, 0xf8841ec9, 0x00000000, 0x09808683, 0x322bed48, 0x1e1170ac, 0x6c5a724e, 0xfd0efffb, 0x0f853856, 0x3daed51e, 0x362d3927, 0x0a0fd964, 0x685ca621, 0x9b5b54d1, 0x24362e3a, 0x0c0a67b1, 0x9357e70f, 0xb4ee96d2, 0x1b9b919e, 0x80c0c54f, 0x61dc20a2, 0x5a774b69, 0x1c121a16, 0xe293ba0a, 0xc0a02ae5, 0x3c22e043, 0x121b171d, 0x0e090d0b, 0xf28bc7ad, 0x2db6a8b9, 0x141ea9c8, 0x57f11985, 0xaf75074c, 0xee99ddbb, 0xa37f60fd, 0xf701269f, 0x5c72f5bc, 0x44663bc5, 0x5bfb7e34, 0x8b432976, 0xcb23c6dc, 0xb6edfc68, 0xb8e4f163, 0xd731dcca, 0x42638510, 0x13972240, 0x84c61120, 0x854a247d, 0xd2bb3df8, 0xaef93211, 0xc729a16d, 0x1d9e2f4b, 0xdcb230f3, 0x0d8652ec, 0x77c1e3d0, 0x2bb3166c, 0xa970b999, 0x119448fa, 0x47e96422, 0xa8fc8cc4, 0xa0f03f1a, 0x567d2cd8, 0x223390ef, 0x87494ec7, 0xd938d1c1, 0x8ccaa2fe, 0x98d40b36, 0xa6f581cf, 0xa57ade28, 0xdab78e26, 0x3fadbfa4, 0x2c3a9de4, 0x5078920d, 0x6a5fcc9b, 0x547e4662, 0xf68d13c2, 0x90d8b8e8, 0x2e39f75e, 0x82c3aff5, 0x9f5d80be, 0x69d0937c, 0x6fd52da9, 0xcf2512b3, 0xc8ac993b, 0x10187da7, 0xe89c636e, 0xdb3bbb7b, 0xcd267809, 0x6e5918f4, 0xec9ab701, 0x834f9aa8, 0xe6956e65, 0xaaffe67e, 0x21bccf08, 0xef15e8e6, 0xbae79bd9, 0x4a6f36ce, 0xea9f09d4, 0x29b07cd6, 0x31a4b2af, 0x2a3f2331, 0xc6a59430, 0x35a266c0, 0x744ebc37, 0xfc82caa6, 0xe090d0b0, 0x33a7d815, 0xf104984a, 0x41ecdaf7, 0x7fcd500e, 0x1791f62f, 0x764dd68d, 0x43efb04d, 0xccaa4d54, 0xe49604df, 0x9ed1b5e3, 0x4c6a881b, 0xc12c1fb8, 0x4665517f, 0x9d5eea04, 0x018c355d, 0xfa877473, 0xfb0b412e, 0xb3671d5a, 0x92dbd252, 0xe9105633, 0x6dd64713, 0x9ad7618c, 0x37a10c7a, 0x59f8148e, 0xeb133c89, 0xcea927ee, 0xb761c935, 0xe11ce5ed, 0x7a47b13c, 0x9cd2df59, 0x55f2733f, 0x1814ce79, 0x73c737bf, 0x53f7cdea, 0x5ffdaa5b, 0xdf3d6f14, 0x7844db86, 0xcaaff381, 0xb968c43e, 0x3824342c, 0xc2a3405f, 0x161dc372, 0xbce2250c, 0x283c498b, 0xff0d9541, 0x39a80171, 0x080cb3de, 0xd8b4e49c, 0x6456c190, 0x7bcb8461, 0xd532b670, 0x486c5c74, 0xd0b85742]);
        T6 = new Uint32Array([0x5051f4a7, 0x537e4165, 0xc31a17a4, 0x963a275e, 0xcb3bab6b, 0xf11f9d45, 0xabacfa58, 0x934be303, 0x552030fa, 0xf6ad766d, 0x9188cc76, 0x25f5024c, 0xfc4fe5d7, 0xd7c52acb, 0x80263544, 0x8fb562a3, 0x49deb15a, 0x6725ba1b, 0x9845ea0e, 0xe15dfec0, 0x02c32f75, 0x12814cf0, 0xa38d4697, 0xc66bd3f9, 0xe7038f5f, 0x9515929c, 0xebbf6d7a, 0xda955259, 0x2dd4be83, 0xd3587421, 0x2949e069, 0x448ec9c8, 0x6a75c289, 0x78f48e79, 0x6b99583e, 0xdd27b971, 0xb6bee14f, 0x17f088ad, 0x66c920ac, 0xb47dce3a, 0x1863df4a, 0x82e51a31, 0x60975133, 0x4562537f, 0xe0b16477, 0x84bb6bae, 0x1cfe81a0, 0x94f9082b, 0x58704868, 0x198f45fd, 0x8794de6c, 0xb7527bf8, 0x23ab73d3, 0xe2724b02, 0x57e31f8f, 0x2a6655ab, 0x07b2eb28, 0x032fb5c2, 0x9a86c57b, 0xa5d33708, 0xf2302887, 0xb223bfa5, 0xba02036a, 0x5ced1682, 0x2b8acf1c, 0x92a779b4, 0xf0f307f2, 0xa14e69e2, 0xcd65daf4, 0xd50605be, 0x1fd13462, 0x8ac4a6fe, 0x9d342e53, 0xa0a2f355, 0x32058ae1, 0x75a4f6eb, 0x390b83ec, 0xaa4060ef, 0x065e719f, 0x51bd6e10, 0xf93e218a, 0x3d96dd06, 0xaedd3e05, 0x464de6bd, 0xb591548d, 0x0571c45d, 0x6f0406d4, 0xff605015, 0x241998fb, 0x97d6bde9, 0xcc894043, 0x7767d99e, 0xbdb0e842, 0x8807898b, 0x38e7195b, 0xdb79c8ee, 0x47a17c0a, 0xe97c420f, 0xc9f8841e, 0x00000000, 0x83098086, 0x48322bed, 0xac1e1170, 0x4e6c5a72, 0xfbfd0eff, 0x560f8538, 0x1e3daed5, 0x27362d39, 0x640a0fd9, 0x21685ca6, 0xd19b5b54, 0x3a24362e, 0xb10c0a67, 0x0f9357e7, 0xd2b4ee96, 0x9e1b9b91, 0x4f80c0c5, 0xa261dc20, 0x695a774b, 0x161c121a, 0x0ae293ba, 0xe5c0a02a, 0x433c22e0, 0x1d121b17, 0x0b0e090d, 0xadf28bc7, 0xb92db6a8, 0xc8141ea9, 0x8557f119, 0x4caf7507, 0xbbee99dd, 0xfda37f60, 0x9ff70126, 0xbc5c72f5, 0xc544663b, 0x345bfb7e, 0x768b4329, 0xdccb23c6, 0x68b6edfc, 0x63b8e4f1, 0xcad731dc, 0x10426385, 0x40139722, 0x2084c611, 0x7d854a24, 0xf8d2bb3d, 0x11aef932, 0x6dc729a1, 0x4b1d9e2f, 0xf3dcb230, 0xec0d8652, 0xd077c1e3, 0x6c2bb316, 0x99a970b9, 0xfa119448, 0x2247e964, 0xc4a8fc8c, 0x1aa0f03f, 0xd8567d2c, 0xef223390, 0xc787494e, 0xc1d938d1, 0xfe8ccaa2, 0x3698d40b, 0xcfa6f581, 0x28a57ade, 0x26dab78e, 0xa43fadbf, 0xe42c3a9d, 0x0d507892, 0x9b6a5fcc, 0x62547e46, 0xc2f68d13, 0xe890d8b8, 0x5e2e39f7, 0xf582c3af, 0xbe9f5d80, 0x7c69d093, 0xa96fd52d, 0xb3cf2512, 0x3bc8ac99, 0xa710187d, 0x6ee89c63, 0x7bdb3bbb, 0x09cd2678, 0xf46e5918, 0x01ec9ab7, 0xa8834f9a, 0x65e6956e, 0x7eaaffe6, 0x0821bccf, 0xe6ef15e8, 0xd9bae79b, 0xce4a6f36, 0xd4ea9f09, 0xd629b07c, 0xaf31a4b2, 0x312a3f23, 0x30c6a594, 0xc035a266, 0x37744ebc, 0xa6fc82ca, 0xb0e090d0, 0x1533a7d8, 0x4af10498, 0xf741ecda, 0x0e7fcd50, 0x2f1791f6, 0x8d764dd6, 0x4d43efb0, 0x54ccaa4d, 0xdfe49604, 0xe39ed1b5, 0x1b4c6a88, 0xb8c12c1f, 0x7f466551, 0x049d5eea, 0x5d018c35, 0x73fa8774, 0x2efb0b41, 0x5ab3671d, 0x5292dbd2, 0x33e91056, 0x136dd647, 0x8c9ad761, 0x7a37a10c, 0x8e59f814, 0x89eb133c, 0xeecea927, 0x35b761c9, 0xede11ce5, 0x3c7a47b1, 0x599cd2df, 0x3f55f273, 0x791814ce, 0xbf73c737, 0xea53f7cd, 0x5b5ffdaa, 0x14df3d6f, 0x867844db, 0x81caaff3, 0x3eb968c4, 0x2c382434, 0x5fc2a340, 0x72161dc3, 0x0cbce225, 0x8b283c49, 0x41ff0d95, 0x7139a801, 0xde080cb3, 0x9cd8b4e4, 0x906456c1, 0x617bcb84, 0x70d532b6, 0x74486c5c, 0x42d0b857]);
        T7 = new Uint32Array([0xa75051f4, 0x65537e41, 0xa4c31a17, 0x5e963a27, 0x6bcb3bab, 0x45f11f9d, 0x58abacfa, 0x03934be3, 0xfa552030, 0x6df6ad76, 0x769188cc, 0x4c25f502, 0xd7fc4fe5, 0xcbd7c52a, 0x44802635, 0xa38fb562, 0x5a49deb1, 0x1b6725ba, 0x0e9845ea, 0xc0e15dfe, 0x7502c32f, 0xf012814c, 0x97a38d46, 0xf9c66bd3, 0x5fe7038f, 0x9c951592, 0x7aebbf6d, 0x59da9552, 0x832dd4be, 0x21d35874, 0x692949e0, 0xc8448ec9, 0x896a75c2, 0x7978f48e, 0x3e6b9958, 0x71dd27b9, 0x4fb6bee1, 0xad17f088, 0xac66c920, 0x3ab47dce, 0x4a1863df, 0x3182e51a, 0x33609751, 0x7f456253, 0x77e0b164, 0xae84bb6b, 0xa01cfe81, 0x2b94f908, 0x68587048, 0xfd198f45, 0x6c8794de, 0xf8b7527b, 0xd323ab73, 0x02e2724b, 0x8f57e31f, 0xab2a6655, 0x2807b2eb, 0xc2032fb5, 0x7b9a86c5, 0x08a5d337, 0x87f23028, 0xa5b223bf, 0x6aba0203, 0x825ced16, 0x1c2b8acf, 0xb492a779, 0xf2f0f307, 0xe2a14e69, 0xf4cd65da, 0xbed50605, 0x621fd134, 0xfe8ac4a6, 0x539d342e, 0x55a0a2f3, 0xe132058a, 0xeb75a4f6, 0xec390b83, 0xefaa4060, 0x9f065e71, 0x1051bd6e, 0x8af93e21, 0x063d96dd, 0x05aedd3e, 0xbd464de6, 0x8db59154, 0x5d0571c4, 0xd46f0406, 0x15ff6050, 0xfb241998, 0xe997d6bd, 0x43cc8940, 0x9e7767d9, 0x42bdb0e8, 0x8b880789, 0x5b38e719, 0xeedb79c8, 0x0a47a17c, 0x0fe97c42, 0x1ec9f884, 0x00000000, 0x86830980, 0xed48322b, 0x70ac1e11, 0x724e6c5a, 0xfffbfd0e, 0x38560f85, 0xd51e3dae, 0x3927362d, 0xd9640a0f, 0xa621685c, 0x54d19b5b, 0x2e3a2436, 0x67b10c0a, 0xe70f9357, 0x96d2b4ee, 0x919e1b9b, 0xc54f80c0, 0x20a261dc, 0x4b695a77, 0x1a161c12, 0xba0ae293, 0x2ae5c0a0, 0xe0433c22, 0x171d121b, 0x0d0b0e09, 0xc7adf28b, 0xa8b92db6, 0xa9c8141e, 0x198557f1, 0x074caf75, 0xddbbee99, 0x60fda37f, 0x269ff701, 0xf5bc5c72, 0x3bc54466, 0x7e345bfb, 0x29768b43, 0xc6dccb23, 0xfc68b6ed, 0xf163b8e4, 0xdccad731, 0x85104263, 0x22401397, 0x112084c6, 0x247d854a, 0x3df8d2bb, 0x3211aef9, 0xa16dc729, 0x2f4b1d9e, 0x30f3dcb2, 0x52ec0d86, 0xe3d077c1, 0x166c2bb3, 0xb999a970, 0x48fa1194, 0x642247e9, 0x8cc4a8fc, 0x3f1aa0f0, 0x2cd8567d, 0x90ef2233, 0x4ec78749, 0xd1c1d938, 0xa2fe8cca, 0x0b3698d4, 0x81cfa6f5, 0xde28a57a, 0x8e26dab7, 0xbfa43fad, 0x9de42c3a, 0x920d5078, 0xcc9b6a5f, 0x4662547e, 0x13c2f68d, 0xb8e890d8, 0xf75e2e39, 0xaff582c3, 0x80be9f5d, 0x937c69d0, 0x2da96fd5, 0x12b3cf25, 0x993bc8ac, 0x7da71018, 0x636ee89c, 0xbb7bdb3b, 0x7809cd26, 0x18f46e59, 0xb701ec9a, 0x9aa8834f, 0x6e65e695, 0xe67eaaff, 0xcf0821bc, 0xe8e6ef15, 0x9bd9bae7, 0x36ce4a6f, 0x09d4ea9f, 0x7cd629b0, 0xb2af31a4, 0x23312a3f, 0x9430c6a5, 0x66c035a2, 0xbc37744e, 0xcaa6fc82, 0xd0b0e090, 0xd81533a7, 0x984af104, 0xdaf741ec, 0x500e7fcd, 0xf62f1791, 0xd68d764d, 0xb04d43ef, 0x4d54ccaa, 0x04dfe496, 0xb5e39ed1, 0x881b4c6a, 0x1fb8c12c, 0x517f4665, 0xea049d5e, 0x355d018c, 0x7473fa87, 0x412efb0b, 0x1d5ab367, 0xd25292db, 0x5633e910, 0x47136dd6, 0x618c9ad7, 0x0c7a37a1, 0x148e59f8, 0x3c89eb13, 0x27eecea9, 0xc935b761, 0xe5ede11c, 0xb13c7a47, 0xdf599cd2, 0x733f55f2, 0xce791814, 0x37bf73c7, 0xcdea53f7, 0xaa5b5ffd, 0x6f14df3d, 0xdb867844, 0xf381caaf, 0xc43eb968, 0x342c3824, 0x405fc2a3, 0xc372161d, 0x250cbce2, 0x498b283c, 0x9541ff0d, 0x017139a8, 0xb3de080c, 0xe49cd8b4, 0xc1906456, 0x84617bcb, 0xb670d532, 0x5c74486c, 0x5742d0b8]);
        T8 = new Uint32Array([0xf4a75051, 0x4165537e, 0x17a4c31a, 0x275e963a, 0xab6bcb3b, 0x9d45f11f, 0xfa58abac, 0xe303934b, 0x30fa5520, 0x766df6ad, 0xcc769188, 0x024c25f5, 0xe5d7fc4f, 0x2acbd7c5, 0x35448026, 0x62a38fb5, 0xb15a49de, 0xba1b6725, 0xea0e9845, 0xfec0e15d, 0x2f7502c3, 0x4cf01281, 0x4697a38d, 0xd3f9c66b, 0x8f5fe703, 0x929c9515, 0x6d7aebbf, 0x5259da95, 0xbe832dd4, 0x7421d358, 0xe0692949, 0xc9c8448e, 0xc2896a75, 0x8e7978f4, 0x583e6b99, 0xb971dd27, 0xe14fb6be, 0x88ad17f0, 0x20ac66c9, 0xce3ab47d, 0xdf4a1863, 0x1a3182e5, 0x51336097, 0x537f4562, 0x6477e0b1, 0x6bae84bb, 0x81a01cfe, 0x082b94f9, 0x48685870, 0x45fd198f, 0xde6c8794, 0x7bf8b752, 0x73d323ab, 0x4b02e272, 0x1f8f57e3, 0x55ab2a66, 0xeb2807b2, 0xb5c2032f, 0xc57b9a86, 0x3708a5d3, 0x2887f230, 0xbfa5b223, 0x036aba02, 0x16825ced, 0xcf1c2b8a, 0x79b492a7, 0x07f2f0f3, 0x69e2a14e, 0xdaf4cd65, 0x05bed506, 0x34621fd1, 0xa6fe8ac4, 0x2e539d34, 0xf355a0a2, 0x8ae13205, 0xf6eb75a4, 0x83ec390b, 0x60efaa40, 0x719f065e, 0x6e1051bd, 0x218af93e, 0xdd063d96, 0x3e05aedd, 0xe6bd464d, 0x548db591, 0xc45d0571, 0x06d46f04, 0x5015ff60, 0x98fb2419, 0xbde997d6, 0x4043cc89, 0xd99e7767, 0xe842bdb0, 0x898b8807, 0x195b38e7, 0xc8eedb79, 0x7c0a47a1, 0x420fe97c, 0x841ec9f8, 0x00000000, 0x80868309, 0x2bed4832, 0x1170ac1e, 0x5a724e6c, 0x0efffbfd, 0x8538560f, 0xaed51e3d, 0x2d392736, 0x0fd9640a, 0x5ca62168, 0x5b54d19b, 0x362e3a24, 0x0a67b10c, 0x57e70f93, 0xee96d2b4, 0x9b919e1b, 0xc0c54f80, 0xdc20a261, 0x774b695a, 0x121a161c, 0x93ba0ae2, 0xa02ae5c0, 0x22e0433c, 0x1b171d12, 0x090d0b0e, 0x8bc7adf2, 0xb6a8b92d, 0x1ea9c814, 0xf1198557, 0x75074caf, 0x99ddbbee, 0x7f60fda3, 0x01269ff7, 0x72f5bc5c, 0x663bc544, 0xfb7e345b, 0x4329768b, 0x23c6dccb, 0xedfc68b6, 0xe4f163b8, 0x31dccad7, 0x63851042, 0x97224013, 0xc6112084, 0x4a247d85, 0xbb3df8d2, 0xf93211ae, 0x29a16dc7, 0x9e2f4b1d, 0xb230f3dc, 0x8652ec0d, 0xc1e3d077, 0xb3166c2b, 0x70b999a9, 0x9448fa11, 0xe9642247, 0xfc8cc4a8, 0xf03f1aa0, 0x7d2cd856, 0x3390ef22, 0x494ec787, 0x38d1c1d9, 0xcaa2fe8c, 0xd40b3698, 0xf581cfa6, 0x7ade28a5, 0xb78e26da, 0xadbfa43f, 0x3a9de42c, 0x78920d50, 0x5fcc9b6a, 0x7e466254, 0x8d13c2f6, 0xd8b8e890, 0x39f75e2e, 0xc3aff582, 0x5d80be9f, 0xd0937c69, 0xd52da96f, 0x2512b3cf, 0xac993bc8, 0x187da710, 0x9c636ee8, 0x3bbb7bdb, 0x267809cd, 0x5918f46e, 0x9ab701ec, 0x4f9aa883, 0x956e65e6, 0xffe67eaa, 0xbccf0821, 0x15e8e6ef, 0xe79bd9ba, 0x6f36ce4a, 0x9f09d4ea, 0xb07cd629, 0xa4b2af31, 0x3f23312a, 0xa59430c6, 0xa266c035, 0x4ebc3774, 0x82caa6fc, 0x90d0b0e0, 0xa7d81533, 0x04984af1, 0xecdaf741, 0xcd500e7f, 0x91f62f17, 0x4dd68d76, 0xefb04d43, 0xaa4d54cc, 0x9604dfe4, 0xd1b5e39e, 0x6a881b4c, 0x2c1fb8c1, 0x65517f46, 0x5eea049d, 0x8c355d01, 0x877473fa, 0x0b412efb, 0x671d5ab3, 0xdbd25292, 0x105633e9, 0xd647136d, 0xd7618c9a, 0xa10c7a37, 0xf8148e59, 0x133c89eb, 0xa927eece, 0x61c935b7, 0x1ce5ede1, 0x47b13c7a, 0xd2df599c, 0xf2733f55, 0x14ce7918, 0xc737bf73, 0xf7cdea53, 0xfdaa5b5f, 0x3d6f14df, 0x44db8678, 0xaff381ca, 0x68c43eb9, 0x24342c38, 0xa3405fc2, 0x1dc37216, 0xe2250cbc, 0x3c498b28, 0x0d9541ff, 0xa8017139, 0x0cb3de08, 0xb4e49cd8, 0x56c19064, 0xcb84617b, 0x32b670d5, 0x6c5c7448, 0xb85742d0]);
        U1 = new Uint32Array([0x00000000, 0x0e090d0b, 0x1c121a16, 0x121b171d, 0x3824342c, 0x362d3927, 0x24362e3a, 0x2a3f2331, 0x70486858, 0x7e416553, 0x6c5a724e, 0x62537f45, 0x486c5c74, 0x4665517f, 0x547e4662, 0x5a774b69, 0xe090d0b0, 0xee99ddbb, 0xfc82caa6, 0xf28bc7ad, 0xd8b4e49c, 0xd6bde997, 0xc4a6fe8a, 0xcaaff381, 0x90d8b8e8, 0x9ed1b5e3, 0x8ccaa2fe, 0x82c3aff5, 0xa8fc8cc4, 0xa6f581cf, 0xb4ee96d2, 0xbae79bd9, 0xdb3bbb7b, 0xd532b670, 0xc729a16d, 0xc920ac66, 0xe31f8f57, 0xed16825c, 0xff0d9541, 0xf104984a, 0xab73d323, 0xa57ade28, 0xb761c935, 0xb968c43e, 0x9357e70f, 0x9d5eea04, 0x8f45fd19, 0x814cf012, 0x3bab6bcb, 0x35a266c0, 0x27b971dd, 0x29b07cd6, 0x038f5fe7, 0x0d8652ec, 0x1f9d45f1, 0x119448fa, 0x4be30393, 0x45ea0e98, 0x57f11985, 0x59f8148e, 0x73c737bf, 0x7dce3ab4, 0x6fd52da9, 0x61dc20a2, 0xad766df6, 0xa37f60fd, 0xb16477e0, 0xbf6d7aeb, 0x955259da, 0x9b5b54d1, 0x894043cc, 0x87494ec7, 0xdd3e05ae, 0xd33708a5, 0xc12c1fb8, 0xcf2512b3, 0xe51a3182, 0xeb133c89, 0xf9082b94, 0xf701269f, 0x4de6bd46, 0x43efb04d, 0x51f4a750, 0x5ffdaa5b, 0x75c2896a, 0x7bcb8461, 0x69d0937c, 0x67d99e77, 0x3daed51e, 0x33a7d815, 0x21bccf08, 0x2fb5c203, 0x058ae132, 0x0b83ec39, 0x1998fb24, 0x1791f62f, 0x764dd68d, 0x7844db86, 0x6a5fcc9b, 0x6456c190, 0x4e69e2a1, 0x4060efaa, 0x527bf8b7, 0x5c72f5bc, 0x0605bed5, 0x080cb3de, 0x1a17a4c3, 0x141ea9c8, 0x3e218af9, 0x302887f2, 0x223390ef, 0x2c3a9de4, 0x96dd063d, 0x98d40b36, 0x8acf1c2b, 0x84c61120, 0xaef93211, 0xa0f03f1a, 0xb2eb2807, 0xbce2250c, 0xe6956e65, 0xe89c636e, 0xfa877473, 0xf48e7978, 0xdeb15a49, 0xd0b85742, 0xc2a3405f, 0xccaa4d54, 0x41ecdaf7, 0x4fe5d7fc, 0x5dfec0e1, 0x53f7cdea, 0x79c8eedb, 0x77c1e3d0, 0x65daf4cd, 0x6bd3f9c6, 0x31a4b2af, 0x3fadbfa4, 0x2db6a8b9, 0x23bfa5b2, 0x09808683, 0x07898b88, 0x15929c95, 0x1b9b919e, 0xa17c0a47, 0xaf75074c, 0xbd6e1051, 0xb3671d5a, 0x99583e6b, 0x97513360, 0x854a247d, 0x8b432976, 0xd134621f, 0xdf3d6f14, 0xcd267809, 0xc32f7502, 0xe9105633, 0xe7195b38, 0xf5024c25, 0xfb0b412e, 0x9ad7618c, 0x94de6c87, 0x86c57b9a, 0x88cc7691, 0xa2f355a0, 0xacfa58ab, 0xbee14fb6, 0xb0e842bd, 0xea9f09d4, 0xe49604df, 0xf68d13c2, 0xf8841ec9, 0xd2bb3df8, 0xdcb230f3, 0xcea927ee, 0xc0a02ae5, 0x7a47b13c, 0x744ebc37, 0x6655ab2a, 0x685ca621, 0x42638510, 0x4c6a881b, 0x5e719f06, 0x5078920d, 0x0a0fd964, 0x0406d46f, 0x161dc372, 0x1814ce79, 0x322bed48, 0x3c22e043, 0x2e39f75e, 0x2030fa55, 0xec9ab701, 0xe293ba0a, 0xf088ad17, 0xfe81a01c, 0xd4be832d, 0xdab78e26, 0xc8ac993b, 0xc6a59430, 0x9cd2df59, 0x92dbd252, 0x80c0c54f, 0x8ec9c844, 0xa4f6eb75, 0xaaffe67e, 0xb8e4f163, 0xb6edfc68, 0x0c0a67b1, 0x02036aba, 0x10187da7, 0x1e1170ac, 0x342e539d, 0x3a275e96, 0x283c498b, 0x26354480, 0x7c420fe9, 0x724b02e2, 0x605015ff, 0x6e5918f4, 0x44663bc5, 0x4a6f36ce, 0x587421d3, 0x567d2cd8, 0x37a10c7a, 0x39a80171, 0x2bb3166c, 0x25ba1b67, 0x0f853856, 0x018c355d, 0x13972240, 0x1d9e2f4b, 0x47e96422, 0x49e06929, 0x5bfb7e34, 0x55f2733f, 0x7fcd500e, 0x71c45d05, 0x63df4a18, 0x6dd64713, 0xd731dcca, 0xd938d1c1, 0xcb23c6dc, 0xc52acbd7, 0xef15e8e6, 0xe11ce5ed, 0xf307f2f0, 0xfd0efffb, 0xa779b492, 0xa970b999, 0xbb6bae84, 0xb562a38f, 0x9f5d80be, 0x91548db5, 0x834f9aa8, 0x8d4697a3]);
        U2 = new Uint32Array([0x00000000, 0x0b0e090d, 0x161c121a, 0x1d121b17, 0x2c382434, 0x27362d39, 0x3a24362e, 0x312a3f23, 0x58704868, 0x537e4165, 0x4e6c5a72, 0x4562537f, 0x74486c5c, 0x7f466551, 0x62547e46, 0x695a774b, 0xb0e090d0, 0xbbee99dd, 0xa6fc82ca, 0xadf28bc7, 0x9cd8b4e4, 0x97d6bde9, 0x8ac4a6fe, 0x81caaff3, 0xe890d8b8, 0xe39ed1b5, 0xfe8ccaa2, 0xf582c3af, 0xc4a8fc8c, 0xcfa6f581, 0xd2b4ee96, 0xd9bae79b, 0x7bdb3bbb, 0x70d532b6, 0x6dc729a1, 0x66c920ac, 0x57e31f8f, 0x5ced1682, 0x41ff0d95, 0x4af10498, 0x23ab73d3, 0x28a57ade, 0x35b761c9, 0x3eb968c4, 0x0f9357e7, 0x049d5eea, 0x198f45fd, 0x12814cf0, 0xcb3bab6b, 0xc035a266, 0xdd27b971, 0xd629b07c, 0xe7038f5f, 0xec0d8652, 0xf11f9d45, 0xfa119448, 0x934be303, 0x9845ea0e, 0x8557f119, 0x8e59f814, 0xbf73c737, 0xb47dce3a, 0xa96fd52d, 0xa261dc20, 0xf6ad766d, 0xfda37f60, 0xe0b16477, 0xebbf6d7a, 0xda955259, 0xd19b5b54, 0xcc894043, 0xc787494e, 0xaedd3e05, 0xa5d33708, 0xb8c12c1f, 0xb3cf2512, 0x82e51a31, 0x89eb133c, 0x94f9082b, 0x9ff70126, 0x464de6bd, 0x4d43efb0, 0x5051f4a7, 0x5b5ffdaa, 0x6a75c289, 0x617bcb84, 0x7c69d093, 0x7767d99e, 0x1e3daed5, 0x1533a7d8, 0x0821bccf, 0x032fb5c2, 0x32058ae1, 0x390b83ec, 0x241998fb, 0x2f1791f6, 0x8d764dd6, 0x867844db, 0x9b6a5fcc, 0x906456c1, 0xa14e69e2, 0xaa4060ef, 0xb7527bf8, 0xbc5c72f5, 0xd50605be, 0xde080cb3, 0xc31a17a4, 0xc8141ea9, 0xf93e218a, 0xf2302887, 0xef223390, 0xe42c3a9d, 0x3d96dd06, 0x3698d40b, 0x2b8acf1c, 0x2084c611, 0x11aef932, 0x1aa0f03f, 0x07b2eb28, 0x0cbce225, 0x65e6956e, 0x6ee89c63, 0x73fa8774, 0x78f48e79, 0x49deb15a, 0x42d0b857, 0x5fc2a340, 0x54ccaa4d, 0xf741ecda, 0xfc4fe5d7, 0xe15dfec0, 0xea53f7cd, 0xdb79c8ee, 0xd077c1e3, 0xcd65daf4, 0xc66bd3f9, 0xaf31a4b2, 0xa43fadbf, 0xb92db6a8, 0xb223bfa5, 0x83098086, 0x8807898b, 0x9515929c, 0x9e1b9b91, 0x47a17c0a, 0x4caf7507, 0x51bd6e10, 0x5ab3671d, 0x6b99583e, 0x60975133, 0x7d854a24, 0x768b4329, 0x1fd13462, 0x14df3d6f, 0x09cd2678, 0x02c32f75, 0x33e91056, 0x38e7195b, 0x25f5024c, 0x2efb0b41, 0x8c9ad761, 0x8794de6c, 0x9a86c57b, 0x9188cc76, 0xa0a2f355, 0xabacfa58, 0xb6bee14f, 0xbdb0e842, 0xd4ea9f09, 0xdfe49604, 0xc2f68d13, 0xc9f8841e, 0xf8d2bb3d, 0xf3dcb230, 0xeecea927, 0xe5c0a02a, 0x3c7a47b1, 0x37744ebc, 0x2a6655ab, 0x21685ca6, 0x10426385, 0x1b4c6a88, 0x065e719f, 0x0d507892, 0x640a0fd9, 0x6f0406d4, 0x72161dc3, 0x791814ce, 0x48322bed, 0x433c22e0, 0x5e2e39f7, 0x552030fa, 0x01ec9ab7, 0x0ae293ba, 0x17f088ad, 0x1cfe81a0, 0x2dd4be83, 0x26dab78e, 0x3bc8ac99, 0x30c6a594, 0x599cd2df, 0x5292dbd2, 0x4f80c0c5, 0x448ec9c8, 0x75a4f6eb, 0x7eaaffe6, 0x63b8e4f1, 0x68b6edfc, 0xb10c0a67, 0xba02036a, 0xa710187d, 0xac1e1170, 0x9d342e53, 0x963a275e, 0x8b283c49, 0x80263544, 0xe97c420f, 0xe2724b02, 0xff605015, 0xf46e5918, 0xc544663b, 0xce4a6f36, 0xd3587421, 0xd8567d2c, 0x7a37a10c, 0x7139a801, 0x6c2bb316, 0x6725ba1b, 0x560f8538, 0x5d018c35, 0x40139722, 0x4b1d9e2f, 0x2247e964, 0x2949e069, 0x345bfb7e, 0x3f55f273, 0x0e7fcd50, 0x0571c45d, 0x1863df4a, 0x136dd647, 0xcad731dc, 0xc1d938d1, 0xdccb23c6, 0xd7c52acb, 0xe6ef15e8, 0xede11ce5, 0xf0f307f2, 0xfbfd0eff, 0x92a779b4, 0x99a970b9, 0x84bb6bae, 0x8fb562a3, 0xbe9f5d80, 0xb591548d, 0xa8834f9a, 0xa38d4697]);
        U3 = new Uint32Array([0x00000000, 0x0d0b0e09, 0x1a161c12, 0x171d121b, 0x342c3824, 0x3927362d, 0x2e3a2436, 0x23312a3f, 0x68587048, 0x65537e41, 0x724e6c5a, 0x7f456253, 0x5c74486c, 0x517f4665, 0x4662547e, 0x4b695a77, 0xd0b0e090, 0xddbbee99, 0xcaa6fc82, 0xc7adf28b, 0xe49cd8b4, 0xe997d6bd, 0xfe8ac4a6, 0xf381caaf, 0xb8e890d8, 0xb5e39ed1, 0xa2fe8cca, 0xaff582c3, 0x8cc4a8fc, 0x81cfa6f5, 0x96d2b4ee, 0x9bd9bae7, 0xbb7bdb3b, 0xb670d532, 0xa16dc729, 0xac66c920, 0x8f57e31f, 0x825ced16, 0x9541ff0d, 0x984af104, 0xd323ab73, 0xde28a57a, 0xc935b761, 0xc43eb968, 0xe70f9357, 0xea049d5e, 0xfd198f45, 0xf012814c, 0x6bcb3bab, 0x66c035a2, 0x71dd27b9, 0x7cd629b0, 0x5fe7038f, 0x52ec0d86, 0x45f11f9d, 0x48fa1194, 0x03934be3, 0x0e9845ea, 0x198557f1, 0x148e59f8, 0x37bf73c7, 0x3ab47dce, 0x2da96fd5, 0x20a261dc, 0x6df6ad76, 0x60fda37f, 0x77e0b164, 0x7aebbf6d, 0x59da9552, 0x54d19b5b, 0x43cc8940, 0x4ec78749, 0x05aedd3e, 0x08a5d337, 0x1fb8c12c, 0x12b3cf25, 0x3182e51a, 0x3c89eb13, 0x2b94f908, 0x269ff701, 0xbd464de6, 0xb04d43ef, 0xa75051f4, 0xaa5b5ffd, 0x896a75c2, 0x84617bcb, 0x937c69d0, 0x9e7767d9, 0xd51e3dae, 0xd81533a7, 0xcf0821bc, 0xc2032fb5, 0xe132058a, 0xec390b83, 0xfb241998, 0xf62f1791, 0xd68d764d, 0xdb867844, 0xcc9b6a5f, 0xc1906456, 0xe2a14e69, 0xefaa4060, 0xf8b7527b, 0xf5bc5c72, 0xbed50605, 0xb3de080c, 0xa4c31a17, 0xa9c8141e, 0x8af93e21, 0x87f23028, 0x90ef2233, 0x9de42c3a, 0x063d96dd, 0x0b3698d4, 0x1c2b8acf, 0x112084c6, 0x3211aef9, 0x3f1aa0f0, 0x2807b2eb, 0x250cbce2, 0x6e65e695, 0x636ee89c, 0x7473fa87, 0x7978f48e, 0x5a49deb1, 0x5742d0b8, 0x405fc2a3, 0x4d54ccaa, 0xdaf741ec, 0xd7fc4fe5, 0xc0e15dfe, 0xcdea53f7, 0xeedb79c8, 0xe3d077c1, 0xf4cd65da, 0xf9c66bd3, 0xb2af31a4, 0xbfa43fad, 0xa8b92db6, 0xa5b223bf, 0x86830980, 0x8b880789, 0x9c951592, 0x919e1b9b, 0x0a47a17c, 0x074caf75, 0x1051bd6e, 0x1d5ab367, 0x3e6b9958, 0x33609751, 0x247d854a, 0x29768b43, 0x621fd134, 0x6f14df3d, 0x7809cd26, 0x7502c32f, 0x5633e910, 0x5b38e719, 0x4c25f502, 0x412efb0b, 0x618c9ad7, 0x6c8794de, 0x7b9a86c5, 0x769188cc, 0x55a0a2f3, 0x58abacfa, 0x4fb6bee1, 0x42bdb0e8, 0x09d4ea9f, 0x04dfe496, 0x13c2f68d, 0x1ec9f884, 0x3df8d2bb, 0x30f3dcb2, 0x27eecea9, 0x2ae5c0a0, 0xb13c7a47, 0xbc37744e, 0xab2a6655, 0xa621685c, 0x85104263, 0x881b4c6a, 0x9f065e71, 0x920d5078, 0xd9640a0f, 0xd46f0406, 0xc372161d, 0xce791814, 0xed48322b, 0xe0433c22, 0xf75e2e39, 0xfa552030, 0xb701ec9a, 0xba0ae293, 0xad17f088, 0xa01cfe81, 0x832dd4be, 0x8e26dab7, 0x993bc8ac, 0x9430c6a5, 0xdf599cd2, 0xd25292db, 0xc54f80c0, 0xc8448ec9, 0xeb75a4f6, 0xe67eaaff, 0xf163b8e4, 0xfc68b6ed, 0x67b10c0a, 0x6aba0203, 0x7da71018, 0x70ac1e11, 0x539d342e, 0x5e963a27, 0x498b283c, 0x44802635, 0x0fe97c42, 0x02e2724b, 0x15ff6050, 0x18f46e59, 0x3bc54466, 0x36ce4a6f, 0x21d35874, 0x2cd8567d, 0x0c7a37a1, 0x017139a8, 0x166c2bb3, 0x1b6725ba, 0x38560f85, 0x355d018c, 0x22401397, 0x2f4b1d9e, 0x642247e9, 0x692949e0, 0x7e345bfb, 0x733f55f2, 0x500e7fcd, 0x5d0571c4, 0x4a1863df, 0x47136dd6, 0xdccad731, 0xd1c1d938, 0xc6dccb23, 0xcbd7c52a, 0xe8e6ef15, 0xe5ede11c, 0xf2f0f307, 0xfffbfd0e, 0xb492a779, 0xb999a970, 0xae84bb6b, 0xa38fb562, 0x80be9f5d, 0x8db59154, 0x9aa8834f, 0x97a38d46]);
        U4 = new Uint32Array([0x00000000, 0x090d0b0e, 0x121a161c, 0x1b171d12, 0x24342c38, 0x2d392736, 0x362e3a24, 0x3f23312a, 0x48685870, 0x4165537e, 0x5a724e6c, 0x537f4562, 0x6c5c7448, 0x65517f46, 0x7e466254, 0x774b695a, 0x90d0b0e0, 0x99ddbbee, 0x82caa6fc, 0x8bc7adf2, 0xb4e49cd8, 0xbde997d6, 0xa6fe8ac4, 0xaff381ca, 0xd8b8e890, 0xd1b5e39e, 0xcaa2fe8c, 0xc3aff582, 0xfc8cc4a8, 0xf581cfa6, 0xee96d2b4, 0xe79bd9ba, 0x3bbb7bdb, 0x32b670d5, 0x29a16dc7, 0x20ac66c9, 0x1f8f57e3, 0x16825ced, 0x0d9541ff, 0x04984af1, 0x73d323ab, 0x7ade28a5, 0x61c935b7, 0x68c43eb9, 0x57e70f93, 0x5eea049d, 0x45fd198f, 0x4cf01281, 0xab6bcb3b, 0xa266c035, 0xb971dd27, 0xb07cd629, 0x8f5fe703, 0x8652ec0d, 0x9d45f11f, 0x9448fa11, 0xe303934b, 0xea0e9845, 0xf1198557, 0xf8148e59, 0xc737bf73, 0xce3ab47d, 0xd52da96f, 0xdc20a261, 0x766df6ad, 0x7f60fda3, 0x6477e0b1, 0x6d7aebbf, 0x5259da95, 0x5b54d19b, 0x4043cc89, 0x494ec787, 0x3e05aedd, 0x3708a5d3, 0x2c1fb8c1, 0x2512b3cf, 0x1a3182e5, 0x133c89eb, 0x082b94f9, 0x01269ff7, 0xe6bd464d, 0xefb04d43, 0xf4a75051, 0xfdaa5b5f, 0xc2896a75, 0xcb84617b, 0xd0937c69, 0xd99e7767, 0xaed51e3d, 0xa7d81533, 0xbccf0821, 0xb5c2032f, 0x8ae13205, 0x83ec390b, 0x98fb2419, 0x91f62f17, 0x4dd68d76, 0x44db8678, 0x5fcc9b6a, 0x56c19064, 0x69e2a14e, 0x60efaa40, 0x7bf8b752, 0x72f5bc5c, 0x05bed506, 0x0cb3de08, 0x17a4c31a, 0x1ea9c814, 0x218af93e, 0x2887f230, 0x3390ef22, 0x3a9de42c, 0xdd063d96, 0xd40b3698, 0xcf1c2b8a, 0xc6112084, 0xf93211ae, 0xf03f1aa0, 0xeb2807b2, 0xe2250cbc, 0x956e65e6, 0x9c636ee8, 0x877473fa, 0x8e7978f4, 0xb15a49de, 0xb85742d0, 0xa3405fc2, 0xaa4d54cc, 0xecdaf741, 0xe5d7fc4f, 0xfec0e15d, 0xf7cdea53, 0xc8eedb79, 0xc1e3d077, 0xdaf4cd65, 0xd3f9c66b, 0xa4b2af31, 0xadbfa43f, 0xb6a8b92d, 0xbfa5b223, 0x80868309, 0x898b8807, 0x929c9515, 0x9b919e1b, 0x7c0a47a1, 0x75074caf, 0x6e1051bd, 0x671d5ab3, 0x583e6b99, 0x51336097, 0x4a247d85, 0x4329768b, 0x34621fd1, 0x3d6f14df, 0x267809cd, 0x2f7502c3, 0x105633e9, 0x195b38e7, 0x024c25f5, 0x0b412efb, 0xd7618c9a, 0xde6c8794, 0xc57b9a86, 0xcc769188, 0xf355a0a2, 0xfa58abac, 0xe14fb6be, 0xe842bdb0, 0x9f09d4ea, 0x9604dfe4, 0x8d13c2f6, 0x841ec9f8, 0xbb3df8d2, 0xb230f3dc, 0xa927eece, 0xa02ae5c0, 0x47b13c7a, 0x4ebc3774, 0x55ab2a66, 0x5ca62168, 0x63851042, 0x6a881b4c, 0x719f065e, 0x78920d50, 0x0fd9640a, 0x06d46f04, 0x1dc37216, 0x14ce7918, 0x2bed4832, 0x22e0433c, 0x39f75e2e, 0x30fa5520, 0x9ab701ec, 0x93ba0ae2, 0x88ad17f0, 0x81a01cfe, 0xbe832dd4, 0xb78e26da, 0xac993bc8, 0xa59430c6, 0xd2df599c, 0xdbd25292, 0xc0c54f80, 0xc9c8448e, 0xf6eb75a4, 0xffe67eaa, 0xe4f163b8, 0xedfc68b6, 0x0a67b10c, 0x036aba02, 0x187da710, 0x1170ac1e, 0x2e539d34, 0x275e963a, 0x3c498b28, 0x35448026, 0x420fe97c, 0x4b02e272, 0x5015ff60, 0x5918f46e, 0x663bc544, 0x6f36ce4a, 0x7421d358, 0x7d2cd856, 0xa10c7a37, 0xa8017139, 0xb3166c2b, 0xba1b6725, 0x8538560f, 0x8c355d01, 0x97224013, 0x9e2f4b1d, 0xe9642247, 0xe0692949, 0xfb7e345b, 0xf2733f55, 0xcd500e7f, 0xc45d0571, 0xdf4a1863, 0xd647136d, 0x31dccad7, 0x38d1c1d9, 0x23c6dccb, 0x2acbd7c5, 0x15e8e6ef, 0x1ce5ede1, 0x07f2f0f3, 0x0efffbfd, 0x79b492a7, 0x70b999a9, 0x6bae84bb, 0x62a38fb5, 0x5d80be9f, 0x548db591, 0x4f9aa883, 0x4697a38d]);
        function AES() {
            if (this._$rapyd$_object_id === undefined) Object.defineProperty(this, "_$rapyd$_object_id", {"value":++_$rapyd$_object_counter});
            AES.prototype.__init__.apply(this, arguments);
        }
        AES.prototype.__init__ = function __init__(key) {
            var self = this;
            var rounds, round_key_count, KC, tk, index, rconpointer, t, tt, i, r, c;
            self.working_mem = _$rapyd$_list_decorate([ new Uint32Array(4), new Uint32Array(4) ]);
            rounds = number_of_rounds[key.length];
            if (!rounds) {
                throw new ValueError("invalid key size (must be length 16, 24 or 32)");
            }
            self._Ke = [];
            self._Kd = [];
            for (var i = 0; i <= rounds; i++) {
                self._Ke.push(new Uint32Array(4));
                self._Kd.push(new Uint32Array(4));
            }
            round_key_count = (rounds + 1) * 4;
            KC = key.length / 4;
            tk = new Uint32Array(KC);
            convert_to_int32(key, tk);
            index = 0;
            for (var i = 0; i < KC; i++) {
                index = i >> 2;
                self._Ke[index][i % 4] = tk[i];
                self._Kd[rounds - index][i % 4] = tk[i];
            }
            rconpointer = 0;
            t = KC;
            while (t < round_key_count) {
                tt = tk[KC - 1];
                tk[0] ^= S[tt >> 16 & 255] << 24 ^ S[tt >> 8 & 255] << 16 ^ S[tt & 255] << 8 ^ S[tt >> 24 & 255] ^ rcon[rconpointer] << 24;
                rconpointer += 1;
                if ((KC !== 8 && (typeof KC !== "object" || _$rapyd$_not_equals(KC, 8)))) {
                    for (var i = 1; i < KC; i++) {
                        tk[i] ^= tk[i - 1];
                    }
                } else {
                    for (var i = 1; i < (KC / 2); i++) {
                        tk[i] ^= tk[i - 1];
                    }
                    tt = tk[KC / 2 - 1];
                    tk[KC / 2] ^= S[tt & 255] ^ S[tt >> 8 & 255] << 8 ^ S[tt >> 16 & 255] << 16 ^ S[tt >> 24 & 255] << 24;
                    for (var i = (KC / 2) + 1; i < KC; i++) {
                        tk[i] ^= tk[i - 1];
                    }
                }
                i = 0;
                while (i < KC && t < round_key_count) {
                    r = t >> 2;
                    c = t % 4;
                    self._Ke[r][c] = tk[i];
                    self._Kd[rounds - r][c] = tk[i++];
                    t += 1;
                }
            }
            for (var r = 1; r < rounds; r++) {
                for (var c = 0; c < 4; c++) {
                    tt = self._Kd[r][c];
                    self._Kd[r][c] = U1[tt >> 24 & 255] ^ U2[tt >> 16 & 255] ^ U3[tt >> 8 & 255] ^ U4[tt & 255];
                }
            }
        };
        AES.prototype._crypt = function _crypt(ciphertext, offset, encrypt) {
            var self = this;
            var R1, R2, R3, R4, o1, o3, SB, K, rounds, a, t, tt;
            if (encrypt) {
                R1 = T1;
                R2 = T2;
                R3 = T3;
                R4 = T4;
                o1 = 1;
                o3 = 3;
                SB = S;
                K = self._Ke;
            } else {
                R1 = T5;
                R2 = T6;
                R3 = T7;
                R4 = T8;
                o1 = 3;
                o3 = 1;
                SB = Si;
                K = self._Kd;
            }
            rounds = K.length - 1;
            a = self.working_mem[0];
            t = self.working_mem[1];
            for (var i = 0; i < 4; i++) {
                t[i] ^= K[0][i];
            }
            for (var r = 1; r < rounds; r++) {
                for (var i = 0; i < 4; i++) {
                    a[i] = R1[t[i] >> 24 & 255] ^ R2[t[(i + o1) % 4] >> 16 & 255] ^ R3[t[(i + 2) % 4] >> 8 & 255] ^ R4[t[(i + o3) % 4] & 255] ^ K[r][i];
                }
                t.set(a);
            }
            for (var i = 0; i < 4; i++) {
                tt = K[rounds][i];
                ciphertext[offset + 4 * i] = (SB[t[i] >> 24 & 255] ^ tt >> 24) & 255;
                ciphertext[offset + 4 * i + 1] = (SB[t[(i + o1) % 4] >> 16 & 255] ^ tt >> 16) & 255;
                ciphertext[offset + 4 * i + 2] = (SB[t[(i + 2) % 4] >> 8 & 255] ^ tt >> 8) & 255;
                ciphertext[offset + 4 * i + 3] = (SB[t[(i + o3) % 4] & 255] ^ tt) & 255;
            }
        };
        AES.prototype.encrypt = function encrypt(plaintext, ciphertext, offset) {
            var self = this;
            convert_to_int32(plaintext, self.working_mem[1], offset, 16);
            return self._crypt(ciphertext, offset, true);
        };
        AES.prototype.encrypt32 = function encrypt32(plaintext, ciphertext, offset) {
            var self = this;
            self.working_mem[1].set(plaintext);
            return self._crypt(ciphertext, offset, true);
        };
        AES.prototype.decrypt = function decrypt(ciphertext, plaintext, offset) {
            var self = this;
            convert_to_int32(ciphertext, self.working_mem[1], offset, 16);
            return self._crypt(plaintext, offset, false);
        };
        AES.prototype.decrypt32 = function decrypt32(ciphertext, plaintext, offset) {
            var self = this;
            self.working_mem[1].set(ciphertext);
            return self._crypt(plaintext, offset, false);
        };
        AES.prototype.__repr__ = function __repr__ () {
            return "<" + __name__ + "." + "AES" + " #" + this._$rapyd$_object_id + ">";
        };
        AES.prototype.__str__ = function __str__ () {
            return this.__repr__();
        };

        function random_bytes_insecure(sz) {
            var ans;
            ans = new Uint8Array(sz);
            for (var i = 0; i < sz; i++) {
                ans[i] = Math.floor(Math.random() * 256);
            }
            return ans;
        }
        function random_bytes_secure(sz) {
            var ans;
            ans = new Uint8Array(sz);
            crypto.getRandomValues(ans);
            return ans;
        }
        random_bytes = (typeof crypto !== "undefined" && typeof crypto.getRandomValues === "function") ? random_bytes_secure : random_bytes_insecure;
        if (random_bytes === random_bytes_insecure) {
            try {
                noderandom = require("crypto").randomBytes;
                random_bytes = function(sz) {
                    return new Uint8Array(noderandom(sz));
                };
            } catch (_$rapyd$_Exception) {
                print("WARNING: Using insecure RNG for AES");
            }
        }
        function ModeOfOperation() {
            if (this._$rapyd$_object_id === undefined) Object.defineProperty(this, "_$rapyd$_object_id", {"value":++_$rapyd$_object_counter});
            ModeOfOperation.prototype.__init__.apply(this, arguments);
        }
        Object.defineProperties(ModeOfOperation.prototype,  {
            "key_as_js": {
                "enumerable": true, 
                "get": function key_as_js() {
                    var self = this;
                    return typed_array_as_js(self.key);
                }, 
                "set": function () { throw new AttributeError("can't set attribute") }
            }, 
        });
        ModeOfOperation.prototype.__init__ = function __init__(key) {
            var self = this;
            self.key = key || generate_key(32);
            self.aes = new AES(self.key);
        };
        ModeOfOperation.prototype.tag_as_bytes = function tag_as_bytes(tag) {
            var self = this;
            if (tag instanceof Uint8Array) {
                return tag;
            }
            if (!tag) {
                return new Uint8Array(0);
            }
            if (typeof tag === "string") {
                return string_to_bytes(tag);
            }
            throw new TypeError("Invalid tag, must be a string or a Uint8Array");
        };
        ModeOfOperation.prototype.__repr__ = function __repr__ () {
            return "<" + __name__ + "." + "ModeOfOperation" + " #" + this._$rapyd$_object_id + ">";
        };
        ModeOfOperation.prototype.__str__ = function __str__ () {
            return this.__repr__();
        };
        

        function GaloisField() {
            if (this._$rapyd$_object_id === undefined) Object.defineProperty(this, "_$rapyd$_object_id", {"value":++_$rapyd$_object_counter});
            GaloisField.prototype.__init__.apply(this, arguments);
        }
        GaloisField.prototype.__init__ = function __init__(sub_key) {
            var self = this;
            var k32;
            k32 = new Uint32Array(4);
            convert_to_int32(sub_key, k32, 0);
            self.m = self.generate_hash_table(k32);
            self.wmem = new Uint32Array(4);
        };
        GaloisField.prototype.power = function power(x, out) {
            var self = this;
            var lsb;
            lsb = x[3] & 1;
            for (var i = 3; i > 0; --i) {
                out[i] = x[i] >>> 1 | (x[i - 1] & 1) << 31;
            }
            out[0] = x[0] >>> 1;
            if (lsb) {
                out[0] ^= 3774873600;
            }
        };
        GaloisField.prototype.multiply = function multiply(x, y) {
            var self = this;
            var z_i, v_i, x_i;
            z_i = new Uint32Array(4);
            v_i = new Uint32Array(y);
            for (var i = 0; i < 128; ++i) {
                x_i = x[i / 32 | 0] & 1 << 31 - i % 32;
                if (x_i) {
                    z_i[0] ^= v_i[0];
                    z_i[1] ^= v_i[1];
                    z_i[2] ^= v_i[2];
                    z_i[3] ^= v_i[3];
                }
                self.power(v_i, v_i);
            }
            return z_i;
        };
        GaloisField.prototype.generate_sub_hash_table = function generate_sub_hash_table(mid) {
            var self = this;
            var bits, size, half, m, i, m_i, m_j, x, _$rapyd$_chain_assign_temp, y;
            bits = mid.length;
            size = 1 << bits;
            half = size >>> 1;
            m = new Array(size);
            m[half] = new Uint32Array(mid);
            i = half >>> 1;
            while (i > 0) {
                m[i] = new Uint32Array(4);
                self.power(m[2 * i], m[i]);
                i >>= 1;
            }
            i = 2;
            while (i < half) {
                for (var j = 1; j < i; ++j) {
                    m_i = m[i];
                    m_j = m[j];
                    _$rapyd$_chain_assign_temp = new Uint32Array(4);
                    m[i + j] = _$rapyd$_chain_assign_temp;
                    x = _$rapyd$_chain_assign_temp;
;
                    for (var c = 0; c < 4; c++) {
                        x[c] = m_i[c] ^ m_j[c];
                    }
                }
                i *= 2;
            }
            m[0] = new Uint32Array(4);
            for (i = half + 1; i < size; ++i) {
                x = m[i ^ half];
                _$rapyd$_chain_assign_temp = new Uint32Array(4);
                m[i] = _$rapyd$_chain_assign_temp;
                y = _$rapyd$_chain_assign_temp;
;
                for (var c = 0; c < 4; c++) {
                    y[c] = mid[c] ^ x[c];
                }
            }
            return m;
        };
        GaloisField.prototype.generate_hash_table = function generate_hash_table(key_as_int32_array) {
            var self = this;
            var bits, multiplier, per_int, size, ans, tmp, idx, shft;
            bits = key_as_int32_array.length;
            multiplier = 8 / bits;
            per_int = 4 * multiplier;
            size = 16 * multiplier;
            ans = new Array(size);
            for (var i =0; i < size; ++i) {
                tmp = new Uint32Array(4);
                idx = i / per_int | 0;
                shft = (per_int - 1 - i % per_int) * bits;
                tmp[idx] = 1 << bits - 1 << shft;
                ans[i] = self.generate_sub_hash_table(self.multiply(tmp, key_as_int32_array));
            }
            return ans;
        };
        GaloisField.prototype.table_multiply = function table_multiply(x) {
            var self = this;
            var z, idx, x_i, ah;
            z = new Uint32Array(4);
            for (var i = 0; i < 32; ++i) {
                idx = i / 8 | 0;
                x_i = x[idx] >>> (7 - i % 8) * 4 & 15;
                ah = self.m[i][x_i];
                z[0] ^= ah[0];
                z[1] ^= ah[1];
                z[2] ^= ah[2];
                z[3] ^= ah[3];
            }
            return z;
        };
        GaloisField.prototype.ghash = function ghash(x, y) {
            var self = this;
            var z;
            z = self.wmem;
            z[0] = y[0] ^ x[0];
            z[1] = y[1] ^ x[1];
            z[2] = y[2] ^ x[2];
            z[3] = y[3] ^ x[3];
            return self.table_multiply(z);
        };
        GaloisField.prototype.__repr__ = function __repr__ () {
            return "<" + __name__ + "." + "GaloisField" + " #" + this._$rapyd$_object_id + ">";
        };
        GaloisField.prototype.__str__ = function __str__ () {
            return this.__repr__();
        };

        function generate_key(sz) {
            if (!number_of_rounds[sz]) {
                throw new ValueError("Invalid key size, must be: 16, 24 or 32");
            }
            return random_bytes(sz);
        }
        function generate_tag(sz) {
            return random_bytes(sz || 32);
        }
        function typed_array_as_js(x) {
            var name;
            name = x.constructor.name || "Uint8Array";
            return "(new " + name + "(" + JSON.stringify(Array.prototype.slice.call(x)) + "))";
        }
        function CBC() {
            if (this._$rapyd$_object_id === undefined) Object.defineProperty(this, "_$rapyd$_object_id", {"value":++_$rapyd$_object_counter});
            CBC.prototype.__init__.apply(this, arguments);
        }
        _$rapyd$_extends(CBC, ModeOfOperation);
        CBC.prototype.__init__ = function __init__ () {
            ModeOfOperation.prototype.__init__ && ModeOfOperation.prototype.__init__.apply(this, arguments);
        };
        CBC.prototype.encrypt_bytes = function encrypt_bytes(bytes, tag_bytes, iv) {
            var self = this;
            var first_iv, _$rapyd$_chain_assign_temp, mlen, padsz, inputbytes, offset, outputbytes, _$rapyd$_unpack;
            _$rapyd$_chain_assign_temp = iv || random_bytes(16);
            iv = _$rapyd$_chain_assign_temp;
            first_iv = _$rapyd$_chain_assign_temp;
;
            mlen = bytes.length + tag_bytes.length;
            padsz = (16 - mlen % 16) % 16;
            inputbytes = new Uint8Array(mlen + padsz);
            if (tag_bytes.length) {
                inputbytes.set(tag_bytes);
            }
            inputbytes.set(bytes, tag_bytes.length);
            offset = 0;
            outputbytes = new Uint8Array(inputbytes.length);
            for (var block = 0; block < inputbytes.length; block += 16) {
                if (block > 0) {
                    _$rapyd$_unpack = [outputbytes, block - 16];
                    iv = _$rapyd$_unpack[0];
                    offset = _$rapyd$_unpack[1];
                }
                for (var i = 0; i < 16; i++) {
                    inputbytes[block + i] ^= iv[offset + i];
                }
                self.aes.encrypt(inputbytes, outputbytes, block);
            }
            return {
                "iv": first_iv,
                "cipherbytes": outputbytes
            };
        };
        CBC.prototype.encrypt = function encrypt(plaintext, tag) {
            var self = this;
            return self.encrypt_bytes(string_to_bytes(plaintext), self.tag_as_bytes(tag));
        };
        CBC.prototype.decrypt_bytes = function decrypt_bytes(inputbytes, tag_bytes, iv) {
            var self = this;
            var offset, outputbytes, _$rapyd$_unpack;
            offset = 0;
            outputbytes = new Uint8Array(inputbytes.length);
            for (var block = 0; block < inputbytes.length; block += 16) {
                self.aes.decrypt(inputbytes, outputbytes, block);
                if (block > 0) {
                    _$rapyd$_unpack = [inputbytes, block - 16];
                    iv = _$rapyd$_unpack[0];
                    offset = _$rapyd$_unpack[1];
                }
                for (var i = 0; i < 16; i++) {
                    outputbytes[block + i] ^= iv[offset + i];
                }
            }
            for (var i = 0; i < tag_bytes.length; i++) {
                if ((tag_bytes[i] !== outputbytes[i] && (typeof tag_bytes[i] !== "object" || _$rapyd$_not_equals(tag_bytes[i], outputbytes[i])))) {
                    throw new ValueError("Corrupt message");
                }
            }
            outputbytes = outputbytes.subarray(tag_bytes.length);
            return outputbytes;
        };
        CBC.prototype.decrypt = function decrypt(output_from_encrypt, tag) {
            var self = this;
            var ans;
            ans = self.decrypt_bytes(output_from_encrypt.cipherbytes, self.tag_as_bytes(tag), output_from_encrypt.iv);
            return str.rstrip(bytes_to_string(ans), "\u0000");
        };
        CBC.prototype.__repr__ = function __repr__ () {
            return "<" + __name__ + "." + "CBC" + " #" + this._$rapyd$_object_id + ">";
        };
        CBC.prototype.__str__ = function __str__ () {
            return this.__repr__();
        };

        function CTR() {
            if (this._$rapyd$_object_id === undefined) Object.defineProperty(this, "_$rapyd$_object_id", {"value":++_$rapyd$_object_counter});
            CTR.prototype.__init__.apply(this, arguments);
        }
        _$rapyd$_extends(CTR, ModeOfOperation);
        CTR.prototype.__init__ = function __init__(key, iv) {
            var self = this;
            ModeOfOperation.prototype.constructor.call(self, key);
            self.wmem = new Uint8Array(16);
            self.counter_block = new Uint8Array(iv || 16);
            if ((self.counter_block.length !== 16 && (typeof self.counter_block.length !== "object" || _$rapyd$_not_equals(self.counter_block.length, 16)))) {
                throw new ValueError("iv must be 16 bytes long");
            }
            self.counter_index = 16;
        };
        CTR.prototype._crypt = function _crypt(bytes) {
            var self = this;
            for (var i = 0; i < bytes.length; i++, self.counter_index++) {
                if (self.counter_index === 16) {
                    self.counter_index = 0;
                    self.aes.encrypt(self.counter_block, self.wmem, 0);
                    increment_counter(self.counter_block);
                }
                bytes[i] ^= self.wmem[self.counter_index];
            }
            self.counter_index = 16;
        };
        CTR.prototype.encrypt = function encrypt(plaintext, tag) {
            var self = this;
            var outbytes, counterbytes, tag_bytes, t;
            outbytes = string_to_bytes(plaintext);
            counterbytes = new Uint8Array(self.counter_block);
            if (tag) {
                tag_bytes = self.tag_as_bytes(tag);
                t = new Uint8Array(outbytes.length + tag_bytes.length);
                t.set(tag_bytes);
                t.set(outbytes, tag_bytes.length);
                outbytes = t;
            }
            self._crypt(outbytes);
            return {
                "cipherbytes": outbytes,
                "counterbytes": counterbytes
            };
        };
        CTR.prototype.__enter__ = function __enter__() {
            var self = this;
            self.before_index = self.counter_index;
            self.before_counter = new Uint8Array(self.counter_block);
        };
        CTR.prototype.__exit__ = function __exit__() {
            var self = this;
            self.counter_index = self.before_index;
            self.counter_block = self.before_counter;
        };
        CTR.prototype.decrypt = function decrypt(output_from_encrypt, tag) {
            var self = this;
            var b, _$rapyd$_with_exception, _$rapyd$_with_suppress, offset, tag_bytes;
            b = new Uint8Array(output_from_encrypt.cipherbytes);
            _$rapyd$_with_exception = undefined;
            var _$rapyd$_with_clause_1 = self;
            _$rapyd$_with_clause_1.__enter__();
            try {
                {
                    self.counter_block = output_from_encrypt.counterbytes;
                    self.counter_index = 16;
                    self._crypt(b);
                }
            } catch(e){
                _$rapyd$_with_exception = e;
            }
            if (_$rapyd$_with_exception === undefined){
                _$rapyd$_with_clause_1.__exit__();
            } else {
                _$rapyd$_with_suppress = false;
                _$rapyd$_with_suppress |= _$rapyd$_bool(_$rapyd$_with_clause_1.__exit__(_$rapyd$_with_exception.constructor, _$rapyd$_with_exception, _$rapyd$_with_exception.stack));
                if (!_$rapyd$_with_suppress) throw _$rapyd$_with_exception;
            }
            offset = 0;
            if (tag) {
                tag_bytes = self.tag_as_bytes(tag);
                for (var i = 0; i < tag_bytes.length; i++) {
                    if ((tag_bytes[i] !== b[i] && (typeof tag_bytes[i] !== "object" || _$rapyd$_not_equals(tag_bytes[i], b[i])))) {
                        throw new ValueError("Corrupted message");
                    }
                }
                offset = tag_bytes.length;
            }
            return bytes_to_string(b, offset);
        };
        CTR.prototype.__repr__ = function __repr__ () {
            return "<" + __name__ + "." + "CTR" + " #" + this._$rapyd$_object_id + ">";
        };
        CTR.prototype.__str__ = function __str__ () {
            return this.__repr__();
        };

        function GCM() {
            if (this._$rapyd$_object_id === undefined) Object.defineProperty(this, "_$rapyd$_object_id", {"value":++_$rapyd$_object_counter});
            GCM.prototype.__init__.apply(this, arguments);
        }
        _$rapyd$_extends(GCM, ModeOfOperation);
        GCM.prototype.__init__ = function __init__(key) {
            var self = this;
            var H;
            ModeOfOperation.prototype.constructor.call(self, key);
            H = new Uint8Array(16);
            self.aes.encrypt(new Uint8Array(16), H, 0);
            self.galois = new GaloisField(H);
            self.J0 = new Uint32Array(4);
            self.wmem = new Uint32Array(4);
            self.byte_block = new Uint8Array(16);
        };
        GCM.prototype._create_j0 = function _create_j0(iv) {
            var self = this;
            var J0, tmp;
            J0 = self.J0;
            if (iv.length === 12) {
                convert_to_int32(iv, J0);
                J0[3] = 1;
            } else {
                J0.fill(0);
                tmp = convert_to_int32_pad(iv);
                while (tmp.length) {
                    J0 = self.galois.ghash(J0, tmp);
                    tmp = tmp.subarray(4);
                }
                tmp = new Uint32Array(4);
                tmp.set(from_64_to_32(iv.length * 8), 2);
                J0 = self.galois.ghash(J0, tmp);
            }
            return J0;
        };
        GCM.prototype._start = function _start(iv, additional_data) {
            var self = this;
            var J0, in_block, S, overflow;
            J0 = self._create_j0(iv);
            in_block = new Uint32Array(J0);
            in_block[3] = in_block[3] + 1 & 4294967295;
            S = new Uint32Array(4);
            overflow = additional_data.length % 16;
            for (var i = 0; i < additional_data.length - overflow; i += 16) {
                convert_to_int32(additional_data, self.wmem, i, 16);
                S = self.galois.ghash(S, self.wmem);
            }
            if (overflow) {
                self.byte_block.fill(0);
                self.byte_block.set(additional_data.subarray(additional_data.length - overflow));
                convert_to_int32(self.byte_block, self.wmem);
                S = self.galois.ghash(S, self.wmem);
            }
            return [J0, in_block, S];
        };
        GCM.prototype._finish = function _finish(iv, J0, adata_len, S, outbytes) {
            var self = this;
            var lengths, tag;
            lengths = new Uint32Array(4);
            lengths.set(from_64_to_32(adata_len * 8));
            lengths.set(from_64_to_32(outbytes.length * 8), 2);
            S = self.galois.ghash(S, lengths);
            self.aes.encrypt32(J0, self.byte_block, 0);
            convert_to_int32(self.byte_block, self.wmem);
            tag = new Uint32Array(4);
            for (var i = 0; i < S.length; i++) {
                tag[i] = S[i] ^ self.wmem[i];
            }
            return {
                "iv": iv,
                "cipherbytes": outbytes,
                "tag": tag
            };
        };
        GCM.prototype._crypt = function _crypt(iv, bytes, additional_data, decrypt) {
            var self = this;
            var ghash, outbytes, _$rapyd$_unpack, J0, in_block, S, bb, enc, hash_bytes, counter_index, overflow;
            ghash = self.galois.ghash.bind(self.galois);
            outbytes = new Uint8Array(bytes.length);
            _$rapyd$_unpack = self._start(iv, additional_data);
            J0 = _$rapyd$_unpack[0];
            in_block = _$rapyd$_unpack[1];
            S = _$rapyd$_unpack[2];
            bb = self.byte_block;
            enc = self.aes.encrypt32.bind(self.aes);
            hash_bytes = (decrypt) ? bytes : outbytes;
            for (var i = 0, counter_index = 16; i < bytes.length; i++, counter_index++) {
                if (counter_index === 16) {
                    enc(in_block, bb, 0);
                    in_block[3] = in_block[3] + 1 & 4294967295;
                    counter_index = 0;
                }
                outbytes[i] = bytes[i] ^ bb[counter_index];
                if (counter_index === 15) {
                    convert_to_int32(hash_bytes, self.wmem, i - 15, 16);
                    S = ghash(S, self.wmem);
                }
            }
            overflow = outbytes.length % 16;
            if (overflow) {
                bb.fill(0);
                bb.set(hash_bytes.subarray(hash_bytes.length - overflow));
                convert_to_int32(bb, self.wmem);
                S = ghash(S, self.wmem);
            }
            return self._finish(iv, J0, additional_data.length, S, outbytes);
        };
        GCM.prototype.encrypt = function encrypt(plaintext, tag) {
            var self = this;
            var iv;
            iv = random_bytes(12);
            return self._crypt(iv, string_to_bytes(plaintext), self.tag_as_bytes(tag), false);
        };
        GCM.prototype.decrypt = function decrypt(output_from_encrypt, tag) {
            var self = this;
            var ans;
            if ((output_from_encrypt.tag.length !== 4 && (typeof output_from_encrypt.tag.length !== "object" || _$rapyd$_not_equals(output_from_encrypt.tag.length, 4)))) {
                throw new ValueError("Corrupted message");
            }
            ans = self._crypt(output_from_encrypt.iv, output_from_encrypt.cipherbytes, self.tag_as_bytes(tag), true);
            if ((ans.tag !== output_from_encrypt.tag && (typeof ans.tag !== "object" || _$rapyd$_not_equals(ans.tag, output_from_encrypt.tag)))) {
                throw new ValueError("Corrupted message");
            }
            return bytes_to_string(ans.cipherbytes);
        };
        GCM.prototype.__repr__ = function __repr__ () {
            return "<" + __name__ + "." + "GCM" + " #" + this._$rapyd$_object_id + ">";
        };
        GCM.prototype.__str__ = function __str__ () {
            return this.__repr__();
        };

        _$rapyd$_modules["aes"]["string_to_bytes"] = string_to_bytes;

        _$rapyd$_modules["aes"]["bytes_to_string"] = bytes_to_string;

        _$rapyd$_modules["aes"]["_$rapyd$_chain_assign_temp"] = _$rapyd$_chain_assign_temp;

        _$rapyd$_modules["aes"]["number_of_rounds"] = number_of_rounds;

        _$rapyd$_modules["aes"]["rcon"] = rcon;

        _$rapyd$_modules["aes"]["S"] = S;

        _$rapyd$_modules["aes"]["Si"] = Si;

        _$rapyd$_modules["aes"]["T1"] = T1;

        _$rapyd$_modules["aes"]["T2"] = T2;

        _$rapyd$_modules["aes"]["T3"] = T3;

        _$rapyd$_modules["aes"]["T4"] = T4;

        _$rapyd$_modules["aes"]["T5"] = T5;

        _$rapyd$_modules["aes"]["T6"] = T6;

        _$rapyd$_modules["aes"]["T7"] = T7;

        _$rapyd$_modules["aes"]["T8"] = T8;

        _$rapyd$_modules["aes"]["U1"] = U1;

        _$rapyd$_modules["aes"]["U2"] = U2;

        _$rapyd$_modules["aes"]["U3"] = U3;

        _$rapyd$_modules["aes"]["U4"] = U4;

        _$rapyd$_modules["aes"]["random_bytes"] = random_bytes;

        _$rapyd$_modules["aes"]["noderandom"] = noderandom;

        _$rapyd$_modules["aes"]["string_to_bytes_encoder"] = string_to_bytes_encoder;

        _$rapyd$_modules["aes"]["string_to_bytes_slow"] = string_to_bytes_slow;

        _$rapyd$_modules["aes"]["as_hex"] = as_hex;

        _$rapyd$_modules["aes"]["bytes_to_string_decoder"] = bytes_to_string_decoder;

        _$rapyd$_modules["aes"]["bytes_to_string_slow"] = bytes_to_string_slow;

        _$rapyd$_modules["aes"]["increment_counter"] = increment_counter;

        _$rapyd$_modules["aes"]["convert_to_int32"] = convert_to_int32;

        _$rapyd$_modules["aes"]["convert_to_int32_pad"] = convert_to_int32_pad;

        _$rapyd$_modules["aes"]["from_64_to_32"] = from_64_to_32;

        _$rapyd$_modules["aes"]["AES"] = AES;

        _$rapyd$_modules["aes"]["random_bytes_insecure"] = random_bytes_insecure;

        _$rapyd$_modules["aes"]["random_bytes_secure"] = random_bytes_secure;

        _$rapyd$_modules["aes"]["ModeOfOperation"] = ModeOfOperation;

        _$rapyd$_modules["aes"]["GaloisField"] = GaloisField;

        _$rapyd$_modules["aes"]["generate_key"] = generate_key;

        _$rapyd$_modules["aes"]["generate_tag"] = generate_tag;

        _$rapyd$_modules["aes"]["typed_array_as_js"] = typed_array_as_js;

        _$rapyd$_modules["aes"]["CBC"] = CBC;

        _$rapyd$_modules["aes"]["CTR"] = CTR;

        _$rapyd$_modules["aes"]["GCM"] = GCM;
    })();

    (function(){
        var __name__ = "crypto";
        var secret_key, gcm;
        var GCM = _$rapyd$_modules["aes"].GCM;
        
        secret_key = "__SECRET_KEY__";
        gcm = null;
        function initialize(after) {
            var decoded;
            if (_$rapyd$_in("_", secret_key)) {
                throw new Exception("secret key was not generated");
            }
            decoded = new Uint8Array(Math.floor(len(secret_key) / 2));
            for (var i = 0, j = 0; i < secret_key.length; i += 2, j++) {
                decoded[j] = parseInt(secret_key[i] + secret_key[i + 1], 16);
            }
            gcm = new GCM(decoded);
            after();
        }
        function encrypt(text) {
            return gcm.encrypt(text);
        }
        function decrypt(output_from_encrypt) {
            return gcm.decrypt(output_from_encrypt);
        }
        _$rapyd$_modules["crypto"]["secret_key"] = secret_key;

        _$rapyd$_modules["crypto"]["gcm"] = gcm;

        _$rapyd$_modules["crypto"]["initialize"] = initialize;

        _$rapyd$_modules["crypto"]["encrypt"] = encrypt;

        _$rapyd$_modules["crypto"]["decrypt"] = decrypt;
    })();

    (function(){
        var __name__ = "qt";
        var bridge, channel;
        bridge = null;
        channel = null;
        function qt_bridge() {
            return bridge;
        }
        function callback(name, data, console_err) {
            var bridge;
            bridge = qt_bridge();
            if (!bridge) {
                console.error(console_err || "Aborting callback: " + name + " as Qt bridge not available");
            } else {
                bridge.callback(name, JSON.stringify(data));
            }
        }
        function connect_signal(name, func) {
            var bridge, signal;
            bridge = qt_bridge();
            if (!bridge) {
                console.error("Failed to connect signal: " + name + " as Qt bridge not available");
            } else {
                signal = bridge[name];
                if (!signal) {
                    console.error("Failed to connect signal: " + name + " as no signal by that name exists");
                } else {
                    signal.connect(func);
                }
            }
        }
        function connect_bridge(proceed) {
            if (window.self !== window.top) {
                proceed();
                return;
            }
            channel = new QWebChannel(qt.webChannelTransport, function(channel) {
                bridge = channel.objects.bridge;
                proceed();
            });
        }
        _$rapyd$_modules["qt"]["bridge"] = bridge;

        _$rapyd$_modules["qt"]["channel"] = channel;

        _$rapyd$_modules["qt"]["qt_bridge"] = qt_bridge;

        _$rapyd$_modules["qt"]["callback"] = callback;

        _$rapyd$_modules["qt"]["connect_signal"] = connect_signal;

        _$rapyd$_modules["qt"]["connect_bridge"] = connect_bridge;
    })();

    (function(){
        var __name__ = "frames";
        var frame_count, frame_id, _$rapyd$_chain_assign_temp, registered, frame_map, handlers;
        var encrypt = _$rapyd$_modules["crypto"].encrypt;
        var decrypt = _$rapyd$_modules["crypto"].decrypt;
        
        _$rapyd$_chain_assign_temp = 0;
        frame_count = _$rapyd$_chain_assign_temp;
        frame_id = _$rapyd$_chain_assign_temp;
;
        registered = false;
        frame_map = new WeakMap();
        function prepare_message(payload, cont) {
            var c;
            payload = JSON.stringify(payload);
            c = encrypt(payload);
            cont({
                "type": "ͻvise_frame_message",
                "encrypted_payload": c,
                "source_frame_id": frame_id
            });
        }
        function post_message(win, payload) {
            prepare_message(payload, function(msg) {
                win.postMessage(msg, "*");
            });
        }
        function broadcast_message(windows, payload) {
            prepare_message(payload, function(msg) {
                var win;
                var _$rapyd$_Iter0 = _$rapyd$_Iterable(windows);
                for (var _$rapyd$_Index0 = 0; _$rapyd$_Index0 < _$rapyd$_Iter0.length; _$rapyd$_Index0++) {
                    win = _$rapyd$_Iter0[_$rapyd$_Index0];
                    win.postMessage(msg, "*");
                }
            });
        }
        handlers = {};
        function handle_message_from_frame(source, source_id, data) {
            var action, f, args, kw;
            action = data.action;
            if (action === "*register") {
                frame_count += 1;
                frame_map.set(source, frame_count);
                post_message(source, {
                    "action": "*set_id",
                    "value": frame_count
                });
            } else if (action === "*set_id") {
                frame_id = data.value;
            } else {
                f = handlers[action];
                if (f) {
                    args = data.args || _$rapyd$_list_decorate([]);
                    kw = data.kwargs || {};
                    f.apply(this, [frame_id, source_id, source].concat(args).concat([_$rapyd$_desugar_kwargs(kw)]));
                }
            }
        }
        function decode_message(event) {
            var raw, payload;
            if (!event.data || event.data.type !== "ͻvise_frame_message") {
                return;
            }
            try {
                raw = decrypt(event.data.encrypted_payload);
            } catch (_$rapyd$_Exception) {
                if (_$rapyd$_Exception instanceof Exception) {
                    var err = _$rapyd$_Exception;
                    console.error(err.stack);
                    console.error("Failed to decrypt frame message: " + err.message);
                    return;
                } else {
                    throw _$rapyd$_Exception;
                }
            }
            payload = JSON.parse(raw);
            handle_message_from_frame(event.source, event.data.source_frame_id, payload);
        }
        function frame_iter() {
            var marked0$0 = [js_generator].map(_$rapyd$_regenerator.regeneratorRuntime.mark);
            function js_generator() {
                var win, filter_func, _$rapyd$_kwargs_obj, frame, i, _$rapyd$_Index0, args$1$0 = arguments;
            
                return _$rapyd$_regenerator.regeneratorRuntime.wrap(function js_generator$(context$1$0) {
                    while (1) switch (context$1$0.prev = context$1$0.next) {
                    case 0:
                        win = ( 0 === args$1$0.length-1 && args$1$0[args$1$0.length-1] !== null && typeof args$1$0[args$1$0.length-1] === "object" && args$1$0[args$1$0.length-1] [_$rapyd$_kwargs_symbol] === true) ? undefined : args$1$0[0];
                        filter_func = (args$1$0[1] === undefined || ( 1 === args$1$0.length-1 && args$1$0[args$1$0.length-1] !== null && typeof args$1$0[args$1$0.length-1] === "object" && args$1$0[args$1$0.length-1] [_$rapyd$_kwargs_symbol] === true)) ? (null) : args$1$0[1];
                        _$rapyd$_kwargs_obj = args$1$0[args$1$0.length-1];
                        if (_$rapyd$_kwargs_obj === null || typeof _$rapyd$_kwargs_obj !== "object" || _$rapyd$_kwargs_obj [_$rapyd$_kwargs_symbol] !== true) _$rapyd$_kwargs_obj = {};
                        if (Object.prototype.hasOwnProperty.call(_$rapyd$_kwargs_obj, "filter_func")){
                            filter_func = _$rapyd$_kwargs_obj.filter_func;
                        }
                        win = win || window.top;
                        _$rapyd$_Index0 = 0;
                    case 7:
                        if (!(_$rapyd$_Index0 < win.frames.length)) {
                            context$1$0.next = 17;
                            break;
                        }
            
                        i = _$rapyd$_Index0;
                        frame = win.frames[i];
            
                        if (!(filter_func === null || filter_func(frame.frameElement))) {
                            context$1$0.next = 13;
                            break;
                        }
            
                        context$1$0.next = 13;
                        return frame;
                    case 13:
                        return context$1$0.delegateYield(
                            frame_iter(frame, _$rapyd$_desugar_kwargs({filter_func: filter_func})),
                            "t0",
                            14
                        );
                    case 14:
                        _$rapyd$_Index0++;
                        context$1$0.next = 7;
                        break;
                    case 17:
                    case "end":
                        return context$1$0.stop();
                    }
                }, marked0$0[0], this);
            }
            var result = js_generator.apply(this, arguments);
            result.send = result.next;
            return result;
        }
        function frame_for_id(frame_id) {
            var ans, frame;
            if (frame_id === 0) {
                return window.top;
            }
            var _$rapyd$_Iter1 = _$rapyd$_Iterable(frame_iter());
            for (var _$rapyd$_Index1 = 0; _$rapyd$_Index1 < _$rapyd$_Iter1.length; _$rapyd$_Index1++) {
                frame = _$rapyd$_Iter1[_$rapyd$_Index1];
                ans = frame_map.get(frame);
                if (ans !== undefined && ans === frame_id) {
                    return frame;
                }
            }
        }
        function register_frames() {
            if (window.self !== window.top && window.location.href === "about:blank") {
                return;
            }
            if (!registered) {
                registered = true;
                window.addEventListener("message", decode_message, false);
                if (window.self !== window.top) {
                    post_message(window.top, {
                        "action": "*register"
                    });
                }
            }
        }
        function register_handler(name, func) {
            handlers[name] = func;
        }
        function prepare_action(name, args, kwargs) {
            return {
                "action": name,
                "args": args,
                "kwargs": kwargs
            };
        }
        function send_action() {
            var win = ( 0 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [_$rapyd$_kwargs_symbol] === true) ? undefined : arguments[0];
            var name = ( 1 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [_$rapyd$_kwargs_symbol] === true) ? undefined : arguments[1];
            var kwargs = arguments[arguments.length-1];
            if (kwargs === null || typeof kwargs !== "object" || kwargs [_$rapyd$_kwargs_symbol] !== true) kwargs = {};
            var args = Array.prototype.slice.call(arguments, 2 );
            if (kwargs !== null && typeof kwargs === "object" && kwargs [_$rapyd$_kwargs_symbol] === true) args .pop();
            post_message(win, prepare_action(name, args, kwargs));
        }
        function broadcast_action() {
            var windows = ( 0 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [_$rapyd$_kwargs_symbol] === true) ? undefined : arguments[0];
            var name = ( 1 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [_$rapyd$_kwargs_symbol] === true) ? undefined : arguments[1];
            var kwargs = arguments[arguments.length-1];
            if (kwargs === null || typeof kwargs !== "object" || kwargs [_$rapyd$_kwargs_symbol] !== true) kwargs = {};
            var args = Array.prototype.slice.call(arguments, 2 );
            if (kwargs !== null && typeof kwargs === "object" && kwargs [_$rapyd$_kwargs_symbol] === true) args .pop();
            broadcast_message(windows, prepare_action(name, args, kwargs));
        }
        _$rapyd$_modules["frames"]["frame_count"] = frame_count;

        _$rapyd$_modules["frames"]["frame_id"] = frame_id;

        _$rapyd$_modules["frames"]["_$rapyd$_chain_assign_temp"] = _$rapyd$_chain_assign_temp;

        _$rapyd$_modules["frames"]["registered"] = registered;

        _$rapyd$_modules["frames"]["frame_map"] = frame_map;

        _$rapyd$_modules["frames"]["handlers"] = handlers;

        _$rapyd$_modules["frames"]["prepare_message"] = prepare_message;

        _$rapyd$_modules["frames"]["post_message"] = post_message;

        _$rapyd$_modules["frames"]["broadcast_message"] = broadcast_message;

        _$rapyd$_modules["frames"]["handle_message_from_frame"] = handle_message_from_frame;

        _$rapyd$_modules["frames"]["decode_message"] = decode_message;

        _$rapyd$_modules["frames"]["frame_iter"] = frame_iter;

        _$rapyd$_modules["frames"]["frame_for_id"] = frame_for_id;

        _$rapyd$_modules["frames"]["register_frames"] = register_frames;

        _$rapyd$_modules["frames"]["register_handler"] = register_handler;

        _$rapyd$_modules["frames"]["prepare_action"] = prepare_action;

        _$rapyd$_modules["frames"]["send_action"] = send_action;

        _$rapyd$_modules["frames"]["broadcast_action"] = broadcast_action;
    })();

    (function(){
        var __name__ = "middle_click";
        var qt_bridge = _$rapyd$_modules["qt"].qt_bridge;
        
        var send_action = _$rapyd$_modules["frames"].send_action;
        var register_handler = _$rapyd$_modules["frames"].register_handler;
        
        function find_link(node) {
            if (node && node.nodeType === Node.ELEMENT_NODE) {
                if (node.nodeName.toUpperCase() === "A" && node.getAttribute("href")) {
                    return node.href;
                }
                return find_link(node.parentElement);
            }
        }
        function middle_clicked(current_frame_id, source_frame_id, source_frame, href) {
            qt_bridge().middle_clicked_link(href);
        }
        function handle_middle_click(ev) {
            var href;
            if (ev.button !== 1) {
                return true;
            }
            href = find_link(ev.target);
            if (!href) {
                return true;
            }
            send_action(window.top, "middle_clicked", href);
            ev.preventDefault();
            ev.stopPropagation();
            return false;
        }
        function onload() {
            register_handler("middle_clicked", middle_clicked);
            document.addEventListener("click", handle_middle_click);
        }
        _$rapyd$_modules["middle_click"]["find_link"] = find_link;

        _$rapyd$_modules["middle_click"]["middle_clicked"] = middle_clicked;

        _$rapyd$_modules["middle_click"]["handle_middle_click"] = handle_middle_click;

        _$rapyd$_modules["middle_click"]["onload"] = onload;
    })();

    (function(){
        var __name__ = "focus";
        var edit_counter;
        var qt_bridge = _$rapyd$_modules["qt"].qt_bridge;
        var connect_signal = _$rapyd$_modules["qt"].connect_signal;
        
        var send_action = _$rapyd$_modules["frames"].send_action;
        var register_handler = _$rapyd$_modules["frames"].register_handler;
        var frame_for_id = _$rapyd$_modules["frames"].frame_for_id;
        
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
        function focus_event_received(current_frame_id, source_frame_id, source_frame, focussed) {
            qt_bridge().element_focused(focussed);
        }
        function handle_focus_in(ev) {
            send_action(window.top, "focus_event_received", is_text_input_node(document.activeElement));
        }
        function handle_focus_out(ev) {
            send_action(window.top, "focus_event_received", false);
        }
        edit_counter = 0;
        function export_edit_text_to_qt(current_frame_id, source_frame_id, source_frame, text, node_id) {
            qt_bridge().edit_text(text, source_frame_id, node_id);
        }
        function find_editable_text(current_frame_id, source_frame_id, source_frame) {
            var elem, text;
            elem = document.activeElement;
            if (elem.contentWindow) {
                send_action(elem.contentWindow, "find_editable_text");
            } else if (is_text_input_node(elem) && text_editing_allowed(elem)) {
                text = elem.value;
                edit_counter += 1;
                elem.setAttribute("data-vise-edit-text", edit_counter + "");
                send_action(window.top, "export_edit_text_to_qt", text || "", edit_counter + "");
            }
        }
        function set_editable_text(text, frame_id, eid) {
            var win;
            win = frame_for_id(frame_id);
            if (!win) {
                console.error("Cannot set editable text, frame with id: " + frame_id + " no longer exists");
                return;
            }
            send_action(win, "set_edit_text", text, eid);
        }
        function set_edit_text(current_frame_id, source_frame_id, source_frame, text, eid) {
            var elem;
            elem = document.querySelector("[data-vise-edit-text=\"" + eid + "\"]");
            if (elem) {
                elem.value = text;
            }
        }
        function onload() {
            document.addEventListener("focusin", handle_focus_in, true);
            document.addEventListener("focusout", handle_focus_out, true);
            if (window.self === window.top) {
                register_handler("focus_event_received", focus_event_received);
                register_handler("export_edit_text_to_qt", export_edit_text_to_qt);
                connect_signal("get_editable_text", function() {
                    send_action(window.top, "find_editable_text");
                });
                connect_signal("set_editable_text", set_editable_text);
            }
            register_handler("find_editable_text", find_editable_text);
            register_handler("set_edit_text", set_edit_text);
        }
        _$rapyd$_modules["focus"]["edit_counter"] = edit_counter;

        _$rapyd$_modules["focus"]["text_editing_allowed"] = text_editing_allowed;

        _$rapyd$_modules["focus"]["is_text_input_node"] = is_text_input_node;

        _$rapyd$_modules["focus"]["focus_event_received"] = focus_event_received;

        _$rapyd$_modules["focus"]["handle_focus_in"] = handle_focus_in;

        _$rapyd$_modules["focus"]["handle_focus_out"] = handle_focus_out;

        _$rapyd$_modules["focus"]["export_edit_text_to_qt"] = export_edit_text_to_qt;

        _$rapyd$_modules["focus"]["find_editable_text"] = find_editable_text;

        _$rapyd$_modules["focus"]["set_editable_text"] = set_editable_text;

        _$rapyd$_modules["focus"]["set_edit_text"] = set_edit_text;

        _$rapyd$_modules["focus"]["onload"] = onload;
    })();

    (function(){
        var __name__ = "elementmaker";
        var html_elements, mathml_elements, svg_elements, html5_tags, E;
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
            s.jsset.add("iframe");
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
        function _makeelement() {
            var tag = ( 0 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [_$rapyd$_kwargs_symbol] === true) ? undefined : arguments[0];
            var kwargs = arguments[arguments.length-1];
            if (kwargs === null || typeof kwargs !== "object" || kwargs [_$rapyd$_kwargs_symbol] !== true) kwargs = {};
            var args = Array.prototype.slice.call(arguments, 1 );
            if (kwargs !== null && typeof kwargs === "object" && kwargs [_$rapyd$_kwargs_symbol] === true) args .pop();
            var ans, vattr, val, attr, arg;
            ans = this.createElement(tag);
            var _$rapyd$_Iter0 = _$rapyd$_Iterable(kwargs);
            for (var _$rapyd$_Index0 = 0; _$rapyd$_Index0 < _$rapyd$_Iter0.length; _$rapyd$_Index0++) {
                attr = _$rapyd$_Iter0[_$rapyd$_Index0];
                vattr = str.replace(str.rstrip(attr, "_"), "_", "-");
                val = kwargs[attr];
                if (callable(val)) {
                    if (str.startswith(attr, "on")) {
                        attr = attr.slice(2);
                    }
                    ans.addEventListener(attr, val);
                } else if (val === true) {
                    ans.setAttribute(vattr, vattr);
                } else if (val !== false) {
                    ans.setAttribute(vattr, val);
                }
            }
            var _$rapyd$_Iter1 = _$rapyd$_Iterable(args);
            for (var _$rapyd$_Index1 = 0; _$rapyd$_Index1 < _$rapyd$_Iter1.length; _$rapyd$_Index1++) {
                arg = _$rapyd$_Iter1[_$rapyd$_Index1];
                if (typeof arg === "string") {
                    arg = this.createTextNode(arg);
                }
                ans.appendChild(arg);
            }
            return ans;
        }
        function maker_for_document(document) {
            var E, tag;
            E = _makeelement.bind(document);
            var _$rapyd$_Iter2 = _$rapyd$_Iterable(html5_tags);
            for (var _$rapyd$_Index2 = 0; _$rapyd$_Index2 < _$rapyd$_Iter2.length; _$rapyd$_Index2++) {
                tag = _$rapyd$_Iter2[_$rapyd$_Index2];
                Object.defineProperty(E, tag, {
                    "value": _makeelement.bind(document, tag)
                });
            }
            return E;
        }
        if (typeof document === "undefined") {
            E = maker_for_document({
                "createTextNode": function(value) {
                    return value;
                },
                "createElement": function(name) {
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
            });
        } else {
            E = maker_for_document(document);
        }
        _$rapyd$_modules["elementmaker"]["html_elements"] = html_elements;

        _$rapyd$_modules["elementmaker"]["mathml_elements"] = mathml_elements;

        _$rapyd$_modules["elementmaker"]["svg_elements"] = svg_elements;

        _$rapyd$_modules["elementmaker"]["html5_tags"] = html5_tags;

        _$rapyd$_modules["elementmaker"]["E"] = E;

        _$rapyd$_modules["elementmaker"]["_makeelement"] = _makeelement;

        _$rapyd$_modules["elementmaker"]["maker_for_document"] = maker_for_document;
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
            var _$rapyd$_unpack, label, minnum;
            var _$rapyd$_Iter0 = _$rapyd$_Iterable(LABELS);
            for (var _$rapyd$_Index0 = 0; _$rapyd$_Index0 < _$rapyd$_Iter0.length; _$rapyd$_Index0++) {
                _$rapyd$_unpack = _$rapyd$_Iter0[_$rapyd$_Index0];
                label = _$rapyd$_unpack[0];
                minnum = _$rapyd$_unpack[1];
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
            update_download(dl_id, "running", -1, -1, 0, 0);
            stop = document.getElementById("stop" + dl_id);
            stop.addEventListener("click", function() {
                cancel_download(dl_id);
            });
        }
        function update_download(dl_id, state, received, total, rate, avg_rate) {
            var status, h, left, fname, text, stop;
            status = document.getElementById("status" + dl_id);
            h = humanize_size;
            if (state === "running") {
                if (received > -1 && total > -1) {
                    if (rate > 0) {
                        left = relative_time(Date.now() + 1e3 * ((total - received) / avg_rate));
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
        var __name__ = "utils";
        function all_frames() {
            var marked0$0 = [js_generator].map(_$rapyd$_regenerator.regeneratorRuntime.mark);
            function js_generator(doc) {
                var stack, document, win, frame, i, _$rapyd$_Index0, e;
            
                return _$rapyd$_regenerator.regeneratorRuntime.wrap(function js_generator$(context$1$0) {
                    while (1) switch (context$1$0.prev = context$1$0.next) {
                    case 0:
                        stack = [doc || window.document];
                    case 1:
                        if (!(stack.length > 0)) {
                            context$1$0.next = 26;
                            break;
                        }
            
                        document = stack.pop();
                        win = document.defaultView;
                        context$1$0.next = 6;
                        return win;
                    case 6:
                        _$rapyd$_Index0 = 0;
                    case 7:
                        if (!(_$rapyd$_Index0 < win.frames.length)) {
                            context$1$0.next = 24;
                            break;
                        }
            
                        i = _$rapyd$_Index0;
                        context$1$0.prev = 9;
                        frame = win.frames[i];
                        if (frame.document !== document) {
                            stack.push(frame.document);
                        }
                        context$1$0.next = 21;
                        break;
                    case 14:
                        context$1$0.prev = 14;
                        context$1$0.t0 = context$1$0["catch"](9);
            
                        if (!(context$1$0.t0 instanceof DOMException)) {
                            context$1$0.next = 20;
                            break;
                        }
            
                        e = context$1$0.t0;
                        context$1$0.next = 21;
                        break;
                    case 20:
                        throw context$1$0.t0;
                    case 21:
                        _$rapyd$_Index0++;
                        context$1$0.next = 7;
                        break;
                    case 24:
                        context$1$0.next = 1;
                        break;
                    case 26:
                    case "end":
                        return context$1$0.stop();
                    }
                }, marked0$0[0], this, [[9, 14]]);
            }
            var result = js_generator.apply(this, arguments);
            result.send = result.next;
            return result;
        }
        function is_visible(elem) {
            var win, rect, child, s;
            if (!elem || !elem.ownerDocument) {
                return false;
            }
            win = elem.ownerDocument.defaultView;
            rect = elem.getBoundingClientRect();
            if (!rect || rect.bottom < 0 || rect.top > win.innerHeight || rect.left > win.innerWidth || rect.right < 0) {
                return false;
            }
            if (!rect.width || !rect.height) {
                var _$rapyd$_Iter0 = _$rapyd$_Iterable(elem.childNodes);
                for (var _$rapyd$_Index0 = 0; _$rapyd$_Index0 < _$rapyd$_Iter0.length; _$rapyd$_Index0++) {
                    child = _$rapyd$_Iter0[_$rapyd$_Index0];
                    if (child.nodeType === child.ELEMENT_NODE && win.getComputedStyle(child).float !== "none" && is_visible(child)) {
                        return true;
                    }
                }
                return false;
            }
            s = win.getComputedStyle(elem);
            if (!s || s.visibility !== "visible" || s.display === "none") {
                return false;
            }
            return true;
        }
        function follow_link() {
            var elem = ( 0 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [_$rapyd$_kwargs_symbol] === true) ? undefined : arguments[0];
            var mouse_button = (arguments[1] === undefined || ( 1 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [_$rapyd$_kwargs_symbol] === true)) ? (0) : arguments[1];
            var _$rapyd$_kwargs_obj = arguments[arguments.length-1];
            if (_$rapyd$_kwargs_obj === null || typeof _$rapyd$_kwargs_obj !== "object" || _$rapyd$_kwargs_obj [_$rapyd$_kwargs_symbol] !== true) _$rapyd$_kwargs_obj = {};
            if (Object.prototype.hasOwnProperty.call(_$rapyd$_kwargs_obj, "mouse_button")){
                mouse_button = _$rapyd$_kwargs_obj.mouse_button;
            }
            var rect, left, top, _$rapyd$_chain_assign_temp, _$rapyd$_unpack, ev;
            elem.focus();
            rect = elem.getBoundingClientRect();
            _$rapyd$_chain_assign_temp = 0;
            left = _$rapyd$_chain_assign_temp;
            top = _$rapyd$_chain_assign_temp;
;
            if (rect) {
                _$rapyd$_unpack = [rect.left, rect.top];
                left = _$rapyd$_unpack[0];
                top = _$rapyd$_unpack[1];
            }
            ev = new MouseEvent("click", {
                "view": elem.ownerDocument.defaultView || window,
                "button": mouse_button,
                "screenX": left,
                "screenY": top,
                "bubbles": true,
                "cancelable": true
            });
            elem.dispatchEvent(ev);
        }
        _$rapyd$_modules["utils"]["all_frames"] = all_frames;

        _$rapyd$_modules["utils"]["is_visible"] = is_visible;

        _$rapyd$_modules["utils"]["follow_link"] = follow_link;
    })();

    (function(){
        var __name__ = "links";
        var is_visible = _$rapyd$_modules["utils"].is_visible;
        
        function iter_links() {
            var marked0$0 = [js_generator].map(_$rapyd$_regenerator.regeneratorRuntime.mark);
            function js_generator() {
                var win, regexps, rel, selector, filter_func, _$rapyd$_kwargs_obj, pat, matches, child, regexp, elem, _$rapyd$_Iter0, _$rapyd$_Index0, _$rapyd$_Iter1, _$rapyd$_Index1, _$rapyd$_Iter2, _$rapyd$_Index2, _$rapyd$_Iter3, _$rapyd$_Index3, args$1$0 = arguments;
            
                return _$rapyd$_regenerator.regeneratorRuntime.wrap(function js_generator$(context$1$0) {
                    while (1) switch (context$1$0.prev = context$1$0.next) {
                    case 0:
                        win = ( 0 === args$1$0.length-1 && args$1$0[args$1$0.length-1] !== null && typeof args$1$0[args$1$0.length-1] === "object" && args$1$0[args$1$0.length-1] [_$rapyd$_kwargs_symbol] === true) ? undefined : args$1$0[0];
                        regexps = (args$1$0[1] === undefined || ( 1 === args$1$0.length-1 && args$1$0[args$1$0.length-1] !== null && typeof args$1$0[args$1$0.length-1] === "object" && args$1$0[args$1$0.length-1] [_$rapyd$_kwargs_symbol] === true)) ? (null) : args$1$0[1];
                        rel = (args$1$0[2] === undefined || ( 2 === args$1$0.length-1 && args$1$0[args$1$0.length-1] !== null && typeof args$1$0[args$1$0.length-1] === "object" && args$1$0[args$1$0.length-1] [_$rapyd$_kwargs_symbol] === true)) ? (null) : args$1$0[2];
                        selector = (args$1$0[3] === undefined || ( 3 === args$1$0.length-1 && args$1$0[args$1$0.length-1] !== null && typeof args$1$0[args$1$0.length-1] === "object" && args$1$0[args$1$0.length-1] [_$rapyd$_kwargs_symbol] === true)) ? (null) : args$1$0[3];
                        filter_func = (args$1$0[4] === undefined || ( 4 === args$1$0.length-1 && args$1$0[args$1$0.length-1] !== null && typeof args$1$0[args$1$0.length-1] === "object" && args$1$0[args$1$0.length-1] [_$rapyd$_kwargs_symbol] === true)) ? (null) : args$1$0[4];
                        _$rapyd$_kwargs_obj = args$1$0[args$1$0.length-1];
                        if (_$rapyd$_kwargs_obj === null || typeof _$rapyd$_kwargs_obj !== "object" || _$rapyd$_kwargs_obj [_$rapyd$_kwargs_symbol] !== true) _$rapyd$_kwargs_obj = {};
                        if (Object.prototype.hasOwnProperty.call(_$rapyd$_kwargs_obj, "regexps")){
                            regexps = _$rapyd$_kwargs_obj.regexps;
                        }
                        if (Object.prototype.hasOwnProperty.call(_$rapyd$_kwargs_obj, "rel")){
                            rel = _$rapyd$_kwargs_obj.rel;
                        }
                        if (Object.prototype.hasOwnProperty.call(_$rapyd$_kwargs_obj, "selector")){
                            selector = _$rapyd$_kwargs_obj.selector;
                        }
                        if (Object.prototype.hasOwnProperty.call(_$rapyd$_kwargs_obj, "filter_func")){
                            filter_func = _$rapyd$_kwargs_obj.filter_func;
                        }
                        selector = selector || ":-webkit-any-link, area, button, iframe, input:not([type=hidden]):not([disabled]), label[for], select, textarea, [onclick], [onmouseover], [onmousedown], [onmouseup], [oncommand], [tabindex], [role=link], [role=button], [contenteditable=true]";
                        win = win || window;
                        if (regexps !== null) {
                            regexps = (function() {
                                var _$rapyd$_Iter = _$rapyd$_Iterable(regexps), _$rapyd$_Result = [], pat;
                                for (var _$rapyd$_Index = 0; _$rapyd$_Index < _$rapyd$_Iter.length; _$rapyd$_Index++) {
                                    pat = _$rapyd$_Iter[_$rapyd$_Index];
                                    _$rapyd$_Result.push((typeof pat === "string") ? new RegExp(pat, "i") : pat);
                                }
                                _$rapyd$_Result = _$rapyd$_list_constructor(_$rapyd$_Result);
                                return _$rapyd$_Result;
                            })();
                        }
                        _$rapyd$_Iter0 = _$rapyd$_Iterable(win.document.querySelectorAll(selector));
                        _$rapyd$_Index0 = 0;
                    case 16:
                        if (!(_$rapyd$_Index0 < _$rapyd$_Iter0.length)) {
                            context$1$0.next = 68;
                            break;
                        }
            
                        elem = _$rapyd$_Iter0[_$rapyd$_Index0];
            
                        if (!(filter_func !== null && !filter_func(elem))) {
                            context$1$0.next = 20;
                            break;
                        }
            
                        return context$1$0.abrupt("continue", 65);
                    case 20:
                        matches = false;
            
                        if (!(rel !== null && elem.getAttribute("rel") === rel)) {
                            context$1$0.next = 25;
                            break;
                        }
            
                        matches = true;
                        context$1$0.next = 62;
                        break;
                    case 25:
                        if (!(regexps === null)) {
                            context$1$0.next = 29;
                            break;
                        }
            
                        matches = true;
                        context$1$0.next = 62;
                        break;
                    case 29:
                        _$rapyd$_Iter1 = _$rapyd$_Iterable(regexps);
                        _$rapyd$_Index1 = 0;
                    case 31:
                        if (!(_$rapyd$_Index1 < _$rapyd$_Iter1.length)) {
                            context$1$0.next = 51;
                            break;
                        }
            
                        regexp = _$rapyd$_Iter1[_$rapyd$_Index1];
            
                        if (!regexp.test(elem.textContent)) {
                            context$1$0.next = 36;
                            break;
                        }
            
                        matches = true;
                        return context$1$0.abrupt("break", 51);
                    case 36:
                        _$rapyd$_Iter2 = _$rapyd$_Iterable(elem.childNodes);
                        _$rapyd$_Index2 = 0;
                    case 38:
                        if (!(_$rapyd$_Index2 < _$rapyd$_Iter2.length)) {
                            context$1$0.next = 46;
                            break;
                        }
            
                        child = _$rapyd$_Iter2[_$rapyd$_Index2];
            
                        if (!regexp.test(child.alt)) {
                            context$1$0.next = 43;
                            break;
                        }
            
                        matches = true;
                        return context$1$0.abrupt("break", 46);
                    case 43:
                        _$rapyd$_Index2++;
                        context$1$0.next = 38;
                        break;
                    case 46:
                        if (!matches) {
                            context$1$0.next = 48;
                            break;
                        }
            
                        return context$1$0.abrupt("break", 51);
                    case 48:
                        _$rapyd$_Index1++;
                        context$1$0.next = 31;
                        break;
                    case 51:
                        if (matches) {
                            context$1$0.next = 62;
                            break;
                        }
            
                        _$rapyd$_Iter3 = _$rapyd$_Iterable(regexps);
                        _$rapyd$_Index3 = 0;
                    case 54:
                        if (!(_$rapyd$_Index3 < _$rapyd$_Iter3.length)) {
                            context$1$0.next = 62;
                            break;
                        }
            
                        regexp = _$rapyd$_Iter3[_$rapyd$_Index3];
            
                        if (!regexp.test(elem.title)) {
                            context$1$0.next = 59;
                            break;
                        }
            
                        matches = true;
                        return context$1$0.abrupt("break", 62);
                    case 59:
                        _$rapyd$_Index3++;
                        context$1$0.next = 54;
                        break;
                    case 62:
                        if (!matches) {
                            context$1$0.next = 65;
                            break;
                        }
            
                        context$1$0.next = 65;
                        return elem;
                    case 65:
                        _$rapyd$_Index0++;
                        context$1$0.next = 16;
                        break;
                    case 68:
                    case "end":
                        return context$1$0.stop();
                    }
                }, marked0$0[0], this);
            }
            var result = js_generator.apply(this, arguments);
            result.send = result.next;
            return result;
        }
        function iter_visible_links() {
            var marked0$0 = [js_generator].map(_$rapyd$_regenerator.regeneratorRuntime.mark);
            function js_generator() {
                var win, regexps, rel, selector, _$rapyd$_kwargs_obj, args$1$0 = arguments;
            
                return _$rapyd$_regenerator.regeneratorRuntime.wrap(function js_generator$(context$1$0) {
                    while (1) switch (context$1$0.prev = context$1$0.next) {
                    case 0:
                        win = ( 0 === args$1$0.length-1 && args$1$0[args$1$0.length-1] !== null && typeof args$1$0[args$1$0.length-1] === "object" && args$1$0[args$1$0.length-1] [_$rapyd$_kwargs_symbol] === true) ? undefined : args$1$0[0];
                        regexps = (args$1$0[1] === undefined || ( 1 === args$1$0.length-1 && args$1$0[args$1$0.length-1] !== null && typeof args$1$0[args$1$0.length-1] === "object" && args$1$0[args$1$0.length-1] [_$rapyd$_kwargs_symbol] === true)) ? (null) : args$1$0[1];
                        rel = (args$1$0[2] === undefined || ( 2 === args$1$0.length-1 && args$1$0[args$1$0.length-1] !== null && typeof args$1$0[args$1$0.length-1] === "object" && args$1$0[args$1$0.length-1] [_$rapyd$_kwargs_symbol] === true)) ? (null) : args$1$0[2];
                        selector = (args$1$0[3] === undefined || ( 3 === args$1$0.length-1 && args$1$0[args$1$0.length-1] !== null && typeof args$1$0[args$1$0.length-1] === "object" && args$1$0[args$1$0.length-1] [_$rapyd$_kwargs_symbol] === true)) ? (null) : args$1$0[3];
                        _$rapyd$_kwargs_obj = args$1$0[args$1$0.length-1];
                        if (_$rapyd$_kwargs_obj === null || typeof _$rapyd$_kwargs_obj !== "object" || _$rapyd$_kwargs_obj [_$rapyd$_kwargs_symbol] !== true) _$rapyd$_kwargs_obj = {};
                        if (Object.prototype.hasOwnProperty.call(_$rapyd$_kwargs_obj, "regexps")){
                            regexps = _$rapyd$_kwargs_obj.regexps;
                        }
                        if (Object.prototype.hasOwnProperty.call(_$rapyd$_kwargs_obj, "rel")){
                            rel = _$rapyd$_kwargs_obj.rel;
                        }
                        if (Object.prototype.hasOwnProperty.call(_$rapyd$_kwargs_obj, "selector")){
                            selector = _$rapyd$_kwargs_obj.selector;
                        }
            
                        return context$1$0.delegateYield(
                            iter_links(win, _$rapyd$_desugar_kwargs({regexps: regexps, selector: selector, rel: rel, filter_func: is_visible})),
                            "t0",
                            10
                        );
                    case 10:
                    case "end":
                        return context$1$0.stop();
                    }
                }, marked0$0[0], this);
            }
            var result = js_generator.apply(this, arguments);
            result.send = result.next;
            return result;
        }
        _$rapyd$_modules["links"]["iter_links"] = iter_links;

        _$rapyd$_modules["links"]["iter_visible_links"] = iter_visible_links;
    })();

    (function(){
        var __name__ = "follow_next";
        var next_regexps, prev_regexps, request_id, request_serviced, current_follow_next_candidate;
        var connect_signal = _$rapyd$_modules["qt"].connect_signal;
        
        var frame_iter = _$rapyd$_modules["frames"].frame_iter;
        var broadcast_action = _$rapyd$_modules["frames"].broadcast_action;
        var send_action = _$rapyd$_modules["frames"].send_action;
        var register_handler = _$rapyd$_modules["frames"].register_handler;
        
        var iter_visible_links = _$rapyd$_modules["links"].iter_visible_links;
        
        var follow_link = _$rapyd$_modules["utils"].follow_link;
        var is_visible = _$rapyd$_modules["utils"].is_visible;
        
        next_regexps = _$rapyd$_list_decorate([ /^\s*Next Page\s*$/i, /^\s*Next [>»]/i, /\bNext\b/i, /^>$/, /^(>>|»)$/, /^(>|»)/, /(>|»)$/, /\bMore\b/i ]);
        prev_regexps = _$rapyd$_list_decorate([ /^\s*Prev(ious)? Page\s*$/i, /[<«] Prev\s*$/i, /\bprev(ious)?\b/i, /^<$/, /^(<<|«)$/, /^(<|«)/, /(<|«)$/ ]);
        request_id = 0;
        request_serviced = false;
        function find_link_in_win(win, forward) {
            var regexps, rel, elem;
            regexps = (forward) ? next_regexps : prev_regexps;
            rel = (forward) ? "next" : "prev";
            var _$rapyd$_Iter0 = _$rapyd$_Iterable(iter_visible_links(win, regexps, rel));
            for (var _$rapyd$_Index0 = 0; _$rapyd$_Index0 < _$rapyd$_Iter0.length; _$rapyd$_Index0++) {
                elem = _$rapyd$_Iter0[_$rapyd$_Index0];
                return elem;
            }
        }
        function follow_next(forward) {
            var elem;
            elem = find_link_in_win(window.self, forward);
            if (elem) {
                follow_link(elem);
            } else {
                request_id += 1;
                request_serviced = false;
                broadcast_action(frame_iter(window.self, is_visible), "follow_next_search", request_id, forward);
            }
        }
        function follow_next_found(current_frame_id, source_frame_id, source_frame, remote_request_id, was_found) {
            var do_it;
            if (!was_found) {
                return;
            }
            do_it = remote_request_id === request_id && !request_serviced;
            send_action(source_frame, "follow_next_execute", remote_request_id, do_it);
            if (do_it) {
                request_serviced = true;
            }
        }
        current_follow_next_candidate = null;
        function follow_next_search(current_frame_id, source_frame_id, source_frame, request_id, forward) {
            var elem;
            elem = find_link_in_win(window.self, forward);
            if (elem) {
                current_follow_next_candidate = [elem, request_id];
            }
            send_action(source_frame, "follow_next_found", request_id, bool(elem));
        }
        function follow_next_execute(current_frame_id, source_frame_id, source_frame, request_id, do_it) {
            var _$rapyd$_unpack, elem, rid;
            if (current_follow_next_candidate) {
                _$rapyd$_unpack = current_follow_next_candidate;
                elem = _$rapyd$_unpack[0];
                rid = _$rapyd$_unpack[1];
                current_follow_next_candidate = null;
                if (do_it && rid === request_id) {
                    follow_link(elem);
                }
            }
        }
        function onload() {
            if (window.self === window.top) {
                connect_signal("follow_next", follow_next);
                register_handler("follow_next_found", follow_next_found);
            } else {
                register_handler("follow_next_search", follow_next_search);
                register_handler("follow_next_execute", follow_next_execute);
            }
        }
        _$rapyd$_modules["follow_next"]["next_regexps"] = next_regexps;

        _$rapyd$_modules["follow_next"]["prev_regexps"] = prev_regexps;

        _$rapyd$_modules["follow_next"]["request_id"] = request_id;

        _$rapyd$_modules["follow_next"]["request_serviced"] = request_serviced;

        _$rapyd$_modules["follow_next"]["current_follow_next_candidate"] = current_follow_next_candidate;

        _$rapyd$_modules["follow_next"]["find_link_in_win"] = find_link_in_win;

        _$rapyd$_modules["follow_next"]["follow_next"] = follow_next;

        _$rapyd$_modules["follow_next"]["follow_next_found"] = follow_next_found;

        _$rapyd$_modules["follow_next"]["follow_next_search"] = follow_next_search;

        _$rapyd$_modules["follow_next"]["follow_next_execute"] = follow_next_execute;

        _$rapyd$_modules["follow_next"]["onload"] = onload;
    })();

    (function(){
        var __name__ = "passwd";
        var input_types, username_names, current_login_form_request_id;
        var send_action = _$rapyd$_modules["frames"].send_action;
        var register_handler = _$rapyd$_modules["frames"].register_handler;
        var broadcast_action = _$rapyd$_modules["frames"].broadcast_action;
        var frame_iter = _$rapyd$_modules["frames"].frame_iter;
        
        var qt_bridge = _$rapyd$_modules["qt"].qt_bridge;
        var connect_signal = _$rapyd$_modules["qt"].connect_signal;
        
        input_types = (function(){
            var s = _$rapyd$_set();
            s.jsset.add("text");
            s.jsset.add("email");
            s.jsset.add("tel");
            return s;
        })();
        username_names = (function(){
            var s = _$rapyd$_set();
            s.jsset.add("login");
            s.jsset.add("user");
            s.jsset.add("mail");
            s.jsset.add("email");
            s.jsset.add("username");
            s.jsset.add("id");
            return s;
        })();
        function form_submitted(ev) {
            var form, _$rapyd$_unpack, username, password;
            form = ev.target;
            _$rapyd$_unpack = get_login_inputs(form);
            username = _$rapyd$_unpack[0];
            password = _$rapyd$_unpack[1];
            if (username !== null) {
                username = username.value;
            }
            if (password !== null) {
                password = password.value;
            }
            send_action(window.top, "login_form_submitted", document.location.href, username, password);
        }
        function get_login_inputs(form) {
            var username, password, _$rapyd$_chain_assign_temp, itype, name, inp;
            _$rapyd$_chain_assign_temp = null;
            username = _$rapyd$_chain_assign_temp;
            password = _$rapyd$_chain_assign_temp;
;
            var _$rapyd$_Iter0 = _$rapyd$_Iterable(form.querySelectorAll("input"));
            for (var _$rapyd$_Index0 = 0; _$rapyd$_Index0 < _$rapyd$_Iter0.length; _$rapyd$_Index0++) {
                inp = _$rapyd$_Iter0[_$rapyd$_Index0];
                if (username !== null && password !== null) {
                    break;
                }
                itype = str.lower(inp.getAttribute("type") || "");
                if (itype === "password") {
                    password = inp;
                } else if (_$rapyd$_in(itype, input_types)) {
                    name = str.lower(inp.name || inp.id || "");
                    if (_$rapyd$_in(name, username_names)) {
                        username = inp;
                    }
                }
            }
            return [username, password];
        }
        function submit_form(form) {
            var buttons;
            buttons = list(form.querySelectorAll("button[type=submit]"));
            if (buttons.length) {
                buttons[buttons.length-1].click();
            } else {
                form.submit();
            }
        }
        function is_login_form(form) {
            var _$rapyd$_unpack, un, pw;
            _$rapyd$_unpack = get_login_inputs(form);
            un = _$rapyd$_unpack[0];
            pw = _$rapyd$_unpack[1];
            return un !== null || pw !== null;
        }
        function login_form_found(current_frame_id, source_frame_id, source_frame, url) {
            qt_bridge().login_form_found_in_page(url);
        }
        function login_form_submitted(current_frame_id, source_frame_id, source_frame, url, username, password) {
            qt_bridge().login_form_submitted_in_page(url, username, password);
        }
        function on_autofill_login_form(url, username, password, autosubmit, is_current_form) {
            if (!do_autofill(url, username, password, autosubmit, is_current_form)) {
                broadcast_action(frame_iter(window.self), "autofill_login_form", url, username, password, autosubmit, is_current_form);
            }
        }
        function autofill_login_form(current_frame_id, source_frame_id, source_frame, url, username, password, autosubmit, is_current_form) {
            do_autofill(url, username, password, autosubmit, is_current_form);
        }
        function do_autofill(url, username, password, autosubmit, is_current_form) {
            var found_form, c, form, _$rapyd$_unpack, un, pw;
            if (url === document.location.href) {
                found_form = null;
                if (is_current_form) {
                    c = document.activeElement;
                    if (c && str.lower(c.tagName) === "input") {
                        while (c.parentNode) {
                            c = c.parentNode;
                            if (str.lower(c.tagName) === "form") {
                                found_form = c;
                                break;
                            }
                        }
                    }
                } else {
                    var _$rapyd$_Iter1 = _$rapyd$_Iterable(document.querySelectorAll("form"));
                    for (var _$rapyd$_Index1 = 0; _$rapyd$_Index1 < _$rapyd$_Iter1.length; _$rapyd$_Index1++) {
                        form = _$rapyd$_Iter1[_$rapyd$_Index1];
                        if (is_login_form(form)) {
                            found_form = form;
                            break;
                        }
                    }
                }
                if (found_form !== null) {
                    _$rapyd$_unpack = get_login_inputs(found_form);
                    un = _$rapyd$_unpack[0];
                    pw = _$rapyd$_unpack[1];
                    if (un !== null && username) {
                        un.value = username;
                    }
                    if (pw !== null && password) {
                        pw.value = password;
                    }
                    if (autosubmit) {
                        submit_form(found_form);
                    }
                    return true;
                }
            }
            return false;
        }
        current_login_form_request_id = 0;
        function on_get_url_for_current_login_form() {
            current_login_form_request_id += 1;
            if (document.activeElement && str.lower(document.activeElement.tagName) === "input") {
                send_action(window.top, "send_url_for_current_login_form", current_login_form_request_id, document.location.href);
            } else {
                broadcast_action(frame_iter(window.self), "get_url_for_current_login_form_in_subframe", current_login_form_request_id);
            }
        }
        function get_url_for_current_login_form_in_subframe(current_frame_id, source_frame_id, source_frame, request_id) {
            if (document.activeElement && str.lower(document.activeElement.tagName) === "input") {
                send_action(window.top, "send_url_for_current_login_form", request_id, document.location.href);
            }
        }
        function send_url_for_current_login_form(current_frame_id, source_frame_id, source_frame, request_id, url) {
            if (request_id === current_login_form_request_id) {
                current_login_form_request_id += 1;
                qt_bridge().url_for_current_login_form(url);
            }
        }
        function onload() {
            var login_forms_found, form;
            if (window === window.top) {
                register_handler("login_form_found", login_form_found);
                register_handler("login_form_submitted", login_form_submitted);
                register_handler("send_url_for_current_login_form", send_url_for_current_login_form);
                connect_signal("autofill_login_form", on_autofill_login_form);
                connect_signal("get_url_for_current_login_form", on_get_url_for_current_login_form);
            } else {
                register_handler("autofill_login_form", autofill_login_form);
                register_handler("get_url_for_current_login_form_in_subframe", get_url_for_current_login_form_in_subframe);
            }
            login_forms_found = false;
            var _$rapyd$_Iter2 = _$rapyd$_Iterable(document.querySelectorAll("form"));
            for (var _$rapyd$_Index2 = 0; _$rapyd$_Index2 < _$rapyd$_Iter2.length; _$rapyd$_Index2++) {
                form = _$rapyd$_Iter2[_$rapyd$_Index2];
                if (is_login_form(form)) {
                    form.addEventListener("submit", form_submitted);
                    login_forms_found = true;
                }
            }
            if (login_forms_found) {
                send_action(window.top, "login_form_found", document.location.href);
            }
        }
        _$rapyd$_modules["passwd"]["input_types"] = input_types;

        _$rapyd$_modules["passwd"]["username_names"] = username_names;

        _$rapyd$_modules["passwd"]["current_login_form_request_id"] = current_login_form_request_id;

        _$rapyd$_modules["passwd"]["form_submitted"] = form_submitted;

        _$rapyd$_modules["passwd"]["get_login_inputs"] = get_login_inputs;

        _$rapyd$_modules["passwd"]["submit_form"] = submit_form;

        _$rapyd$_modules["passwd"]["is_login_form"] = is_login_form;

        _$rapyd$_modules["passwd"]["login_form_found"] = login_form_found;

        _$rapyd$_modules["passwd"]["login_form_submitted"] = login_form_submitted;

        _$rapyd$_modules["passwd"]["on_autofill_login_form"] = on_autofill_login_form;

        _$rapyd$_modules["passwd"]["autofill_login_form"] = autofill_login_form;

        _$rapyd$_modules["passwd"]["do_autofill"] = do_autofill;

        _$rapyd$_modules["passwd"]["on_get_url_for_current_login_form"] = on_get_url_for_current_login_form;

        _$rapyd$_modules["passwd"]["get_url_for_current_login_form_in_subframe"] = get_url_for_current_login_form_in_subframe;

        _$rapyd$_modules["passwd"]["send_url_for_current_login_form"] = send_url_for_current_login_form;

        _$rapyd$_modules["passwd"]["onload"] = onload;
    })();

    (function(){

        var __name__ = "__main__";


        var init_crypto = _$rapyd$_modules["crypto"].initialize;
        
        var connect_bridge = _$rapyd$_modules["qt"].connect_bridge;
        
        var register_frames = _$rapyd$_modules["frames"].register_frames;
        
        var mc_onload = _$rapyd$_modules["middle_click"].onload;
        
        var focus_onload = _$rapyd$_modules["focus"].onload;
        
        var downloads = _$rapyd$_modules["downloads"].main;
        
        var fn_onload = _$rapyd$_modules["follow_next"].onload;
        
        var passwd_onload = _$rapyd$_modules["passwd"].onload;
        
        function on_document_loaded() {
            connect_bridge(function() {
                if (document.location.href === "__DOWNLOADS_URL__") {
                    downloads();
                } else {
                    mc_onload();
                    focus_onload();
                    fn_onload();
                    passwd_onload();
                }
            });
        }
        init_crypto(register_frames);
        document.addEventListener("DOMContentLoaded", on_document_loaded);
    })();
})();
