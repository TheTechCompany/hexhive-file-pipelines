"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var __asyncValues = (this && this.__asyncValues) || function (o) {
    if (!Symbol.asyncIterator) throw new TypeError("Symbol.asyncIterator is not defined.");
    var m = o[Symbol.asyncIterator], i;
    return m ? m.call(o) : (o = typeof __values === "function" ? __values(o) : o[Symbol.iterator](), i = {}, verb("next"), verb("throw"), verb("return"), i[Symbol.asyncIterator] = function () { return this; }, i);
    function verb(n) { i[n] = o[n] && function (v) { return new Promise(function (resolve, reject) { v = o[n](v), settle(resolve, reject, v.done, v.value); }); }; }
    function settle(resolve, reject, d, v) { Promise.resolve(v).then(function(v) { resolve({ value: v, done: d }); }, reject); }
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var ipfs_http_client_1 = __importDefault(require("ipfs-http-client"));
var fs_1 = __importDefault(require("fs"));
exports.default = (function (options) { return __awaiter(void 0, void 0, void 0, function () {
    var node, _a, _b, getFile, addFile;
    return __generator(this, function (_c) {
        switch (_c.label) {
            case 0: return [4 /*yield*/, ipfs_http_client_1.default.create({ url: options.url })];
            case 1:
                node = _c.sent();
                _b = (_a = console).log;
                return [4 /*yield*/, node.id()];
            case 2:
                _b.apply(_a, [_c.sent()]);
                getFile = function (cid, tmpPath) { return __awaiter(void 0, void 0, void 0, function () {
                    var content, chunkCount, _a, _b, chunk, e_1_1;
                    var e_1, _c;
                    return __generator(this, function (_d) {
                        switch (_d.label) {
                            case 0:
                                content = Buffer.from('');
                                chunkCount = 0;
                                _d.label = 1;
                            case 1:
                                _d.trys.push([1, 6, 7, 12]);
                                _a = __asyncValues(node.cat(cid));
                                _d.label = 2;
                            case 2: return [4 /*yield*/, _a.next()];
                            case 3:
                                if (!(_b = _d.sent(), !_b.done)) return [3 /*break*/, 5];
                                chunk = _b.value;
                                // if(chunkCount == 0){
                                // console.log(chunk.toString())
                                //     chunkCount++;
                                // }
                                content = Buffer.concat([content, chunk]);
                                _d.label = 4;
                            case 4: return [3 /*break*/, 2];
                            case 5: return [3 /*break*/, 12];
                            case 6:
                                e_1_1 = _d.sent();
                                e_1 = { error: e_1_1 };
                                return [3 /*break*/, 12];
                            case 7:
                                _d.trys.push([7, , 10, 11]);
                                if (!(_b && !_b.done && (_c = _a.return))) return [3 /*break*/, 9];
                                return [4 /*yield*/, _c.call(_a)];
                            case 8:
                                _d.sent();
                                _d.label = 9;
                            case 9: return [3 /*break*/, 11];
                            case 10:
                                if (e_1) throw e_1.error;
                                return [7 /*endfinally*/];
                            case 11: return [7 /*endfinally*/];
                            case 12:
                                fs_1.default.writeFileSync(tmpPath, content);
                                console.log("Gotten file", cid);
                                return [2 /*return*/];
                        }
                    });
                }); };
                addFile = function (file) { return __awaiter(void 0, void 0, void 0, function () {
                    var result;
                    return __generator(this, function (_a) {
                        switch (_a.label) {
                            case 0:
                                console.log("Adding file");
                                return [4 /*yield*/, node.add(file)];
                            case 1:
                                result = _a.sent();
                                return [2 /*return*/, result.cid];
                        }
                    });
                }); };
                return [2 /*return*/, {
                        addFile: addFile,
                        getFile: getFile
                    }];
        }
    });
}); });
