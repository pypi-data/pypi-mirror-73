/*!
 * Copyright (c) 2012 - 2020, Anaconda, Inc., and Bokeh Contributors
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 * 
 * Redistributions of source code must retain the above copyright notice,
 * this list of conditions and the following disclaimer.
 * 
 * Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 * 
 * Neither the name of Anaconda nor the names of any contributors
 * may be used to endorse or promote products derived from this software
 * without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
 * THE POSSIBILITY OF SUCH DAMAGE.
*/
(function(root, factory) {
  factory(root["Bokeh"], undefined);
})(this, function(Bokeh, version) {
  var define;
  return (function(modules, entry, aliases, externals) {
    const bokeh = typeof Bokeh !== "undefined" && (version != null ? Bokeh[version] : Bokeh);
    if (bokeh != null) {
      return bokeh.register_plugin(modules, entry, aliases);
    } else {
      throw new Error("Cannot find Bokeh " + version + ". You have to load it prior to loading plugins.");
    }
  })
({
485: /* models/glyphs/webgl/main.js */ function _(require, module, exports) {
    Object.defineProperty(exports, "__esModule", { value: true });
    require(486) /* ./index */;
},
486: /* models/glyphs/webgl/index.js */ function _(require, module, exports) {
    Object.defineProperty(exports, "__esModule", { value: true });
    var tslib_1 = require(1) /* tslib */;
    /*
    Copyright notice: many of the awesome techniques and  GLSL code contained in
    this module are based on work by Nicolas Rougier as part of the Glumpy and
    Vispy projects. The algorithms are published in
    http://jcgt.org/published/0003/04/01/ and http://jcgt.org/published/0002/02/08/
    
    This module contains all gl-specific code to add gl support for the glyphs.
    By implementing it separetely, the GL functionality can be spun off in a
    separate library.
    Other locations where we work with GL, or prepare for GL-rendering:
    - canvas.ts
    - plot.ts
    - glyph.ts
    - glyph_renderer.ts
    */
    tslib_1.__exportStar(require(487) /* ./line */, exports);
    tslib_1.__exportStar(require(495) /* ./markers */, exports);
},
487: /* models/glyphs/webgl/line.js */ function _(require, module, exports) {
    Object.defineProperty(exports, "__esModule", { value: true });
    var tslib_1 = require(1) /* tslib */;
    var utils_1 = require(488) /* ./utils */;
    var base_1 = require(492) /* ./base */;
    var line_vert_1 = require(493) /* ./line.vert */;
    var line_frag_1 = require(494) /* ./line.frag */;
    var color_1 = require(135) /* ../../../core/util/color */;
    var DashAtlas = /** @class */ (function () {
        function DashAtlas(gl) {
            this._atlas = new Map();
            this._width = 256;
            this._height = 256;
            // Init texture
            this.tex = new utils_1.Texture2d(gl);
            this.tex.set_wrapping(gl.REPEAT, gl.REPEAT);
            this.tex.set_interpolation(gl.NEAREST, gl.NEAREST);
            this.tex.set_size([this._width, this._height], gl.RGBA);
            this.tex.set_data([0, 0], [this._width, this._height], new Uint8Array(4 * this._width * this._height));
            // Init with solid line (index 0 is reserved for this)
            this.get_atlas_data([1]);
        }
        DashAtlas.prototype.get_atlas_data = function (pattern) {
            var key = pattern.join("-");
            var atlas_data = this._atlas.get(key);
            if (atlas_data == null) {
                var _a = this.make_pattern(pattern), data = _a[0], period = _a[1];
                var index = this._atlas.size;
                this.tex.set_data([0, index], [this._width, 1], new Uint8Array(data.map(function (x) { return x + 10; })));
                atlas_data = [index / this._height, period];
                this._atlas.set(key, atlas_data);
            }
            return atlas_data;
        };
        DashAtlas.prototype.make_pattern = function (pattern) {
            // A pattern is defined as on/off sequence of segments
            // It must be a multiple of 2
            if (pattern.length > 1 && pattern.length % 2) {
                pattern = pattern.concat(pattern);
            }
            // Period is sum of elements
            var period = 0;
            for (var _i = 0, pattern_1 = pattern; _i < pattern_1.length; _i++) {
                var v = pattern_1[_i];
                period += v;
            }
            // Find all start and end of on-segment only
            var C = [];
            var c = 0;
            for (var i = 0, end = pattern.length + 2; i < end; i += 2) {
                var a = Math.max(0.0001, pattern[i % pattern.length]);
                var b = Math.max(0.0001, pattern[(i + 1) % pattern.length]);
                C.push(c, c + a);
                c += a + b;
            }
            // Build pattern
            var n = this._width;
            var Z = new Float32Array(n * 4);
            for (var i = 0, end = n; i < end; i++) {
                var dash_end = void 0, dash_start = void 0, dash_type = void 0;
                var x = (period * i) / (n - 1);
                // get index at min - index = np.argmin(abs(C-(x)))
                var index = 0;
                var val_at_index = 1e16;
                for (var j = 0, endj = C.length; j < endj; j++) {
                    var val = Math.abs(C[j] - x);
                    if (val < val_at_index) {
                        index = j;
                        val_at_index = val;
                    }
                }
                if ((index % 2) === 0) {
                    dash_type = (x <= C[index]) ? +1 : 0;
                    dash_start = C[index];
                    dash_end = C[index + 1];
                }
                else {
                    dash_type = (x > C[index]) ? -1 : 0;
                    dash_start = C[index - 1];
                    dash_end = C[index];
                }
                Z[(i * 4) + 0] = C[index];
                Z[(i * 4) + 1] = dash_type;
                Z[(i * 4) + 2] = dash_start;
                Z[(i * 4) + 3] = dash_end;
            }
            return [Z, period];
        };
        return DashAtlas;
    }());
    DashAtlas.__name__ = "DashAtlas";
    var joins = { miter: 0, round: 1, bevel: 2 };
    var caps = {
        '': 0, none: 0, '.': 0,
        round: 1, ')': 1, '(': 1, o: 1,
        'triangle in': 2, '<': 2,
        'triangle out': 3, '>': 3,
        square: 4, '[': 4, ']': 4, '=': 4,
        butt: 5, '|': 5,
    };
    var LineGLGlyph = /** @class */ (function (_super) {
        tslib_1.__extends(LineGLGlyph, _super);
        function LineGLGlyph() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        LineGLGlyph.prototype.init = function () {
            var gl = this.gl;
            this._scale_aspect = 0; // keep track, so we know when we need to update segment data
            var vert = line_vert_1.vertex_shader;
            var frag = line_frag_1.fragment_shader;
            // The program
            this.prog = new utils_1.Program(gl);
            this.prog.set_shaders(vert, frag);
            this.index_buffer = new utils_1.IndexBuffer(gl);
            // Buffers
            this.vbo_position = new utils_1.VertexBuffer(gl);
            this.vbo_tangents = new utils_1.VertexBuffer(gl);
            this.vbo_segment = new utils_1.VertexBuffer(gl);
            this.vbo_angles = new utils_1.VertexBuffer(gl);
            this.vbo_texcoord = new utils_1.VertexBuffer(gl);
            // Dash atlas
            this.dash_atlas = new DashAtlas(gl);
        };
        LineGLGlyph.prototype.draw = function (indices, mainGlyph, trans) {
            var mainGlGlyph = mainGlyph.glglyph;
            if (mainGlGlyph.data_changed) {
                if (!(isFinite(trans.dx) && isFinite(trans.dy))) {
                    return; // not sure why, but it happens on init sometimes (#4367)
                }
                mainGlGlyph._baked_offset = [trans.dx, trans.dy]; // float32 precision workaround; used in _bake() and below
                mainGlGlyph._set_data();
                mainGlGlyph.data_changed = false;
            }
            if (this.visuals_changed) {
                this._set_visuals();
                this.visuals_changed = false;
            }
            // Decompose x-y scale into scalar scale and aspect-vector.
            var sx = trans.sx, sy = trans.sy;
            var scale_length = Math.sqrt(sx * sx + sy * sy);
            sx /= scale_length;
            sy /= scale_length;
            // Do we need to re-calculate segment data and cumsum?
            if (Math.abs(this._scale_aspect - sy / sx) > Math.abs(1e-3 * this._scale_aspect)) {
                mainGlGlyph._update_scale(sx, sy);
                this._scale_aspect = sy / sx;
            }
            // Select buffers from main glyph
            // (which may be this glyph but maybe not if this is a (non)selection glyph)
            this.prog.set_attribute('a_position', 'vec2', mainGlGlyph.vbo_position);
            this.prog.set_attribute('a_tangents', 'vec4', mainGlGlyph.vbo_tangents);
            this.prog.set_attribute('a_segment', 'vec2', mainGlGlyph.vbo_segment);
            this.prog.set_attribute('a_angles', 'vec2', mainGlGlyph.vbo_angles);
            this.prog.set_attribute('a_texcoord', 'vec2', mainGlGlyph.vbo_texcoord);
            //
            this.prog.set_uniform('u_length', 'float', [mainGlGlyph.cumsum]);
            this.prog.set_texture('u_dash_atlas', this.dash_atlas.tex);
            // Handle transformation to device coordinates
            var baked_offset = mainGlGlyph._baked_offset;
            this.prog.set_uniform('u_pixel_ratio', 'float', [trans.pixel_ratio]);
            this.prog.set_uniform('u_canvas_size', 'vec2', [trans.width, trans.height]);
            this.prog.set_uniform('u_offset', 'vec2', [trans.dx - baked_offset[0], trans.dy - baked_offset[1]]);
            this.prog.set_uniform('u_scale_aspect', 'vec2', [sx, sy]);
            this.prog.set_uniform('u_scale_length', 'float', [scale_length]);
            this.I_triangles = mainGlGlyph.I_triangles;
            if (this.I_triangles.length < 65535) {
                // Data is small enough to draw in one pass
                this.index_buffer.set_size(this.I_triangles.length * 2);
                this.index_buffer.set_data(0, new Uint16Array(this.I_triangles));
                this.prog.draw(this.gl.TRIANGLES, this.index_buffer);
                // @prog.draw(@gl.LINE_STRIP, @index_buffer)  # Use this to draw the line skeleton
            }
            else {
                // Work around the limit that the indexbuffer must be uint16. We draw in chunks.
                // First collect indices in chunks
                indices = Array.from(this.I_triangles);
                var nvertices = this.I_triangles.length;
                var chunksize = 64008; // 65536 max. 64008 is divisible by 12
                var chunks = [];
                for (var i = 0, end = Math.ceil(nvertices / chunksize); i < end; i++) {
                    chunks.push([]);
                }
                for (var i = 0, end = indices.length; i < end; i++) {
                    var uint16_index = indices[i] % chunksize;
                    var chunk = Math.floor(indices[i] / chunksize);
                    chunks[chunk].push(uint16_index);
                }
                // Then draw each chunk
                for (var chunk = 0, end = chunks.length; chunk < end; chunk++) {
                    var these_indices = new Uint16Array(chunks[chunk]);
                    var offset = chunk * chunksize * 4;
                    if (these_indices.length === 0) {
                        continue;
                    }
                    this.prog.set_attribute('a_position', 'vec2', mainGlGlyph.vbo_position, 0, offset * 2);
                    this.prog.set_attribute('a_tangents', 'vec4', mainGlGlyph.vbo_tangents, 0, offset * 4);
                    this.prog.set_attribute('a_segment', 'vec2', mainGlGlyph.vbo_segment, 0, offset * 2);
                    this.prog.set_attribute('a_angles', 'vec2', mainGlGlyph.vbo_angles, 0, offset * 2);
                    this.prog.set_attribute('a_texcoord', 'vec2', mainGlGlyph.vbo_texcoord, 0, offset * 2);
                    // The actual drawing
                    this.index_buffer.set_size(these_indices.length * 2);
                    this.index_buffer.set_data(0, these_indices);
                    this.prog.draw(this.gl.TRIANGLES, this.index_buffer);
                }
            }
        };
        LineGLGlyph.prototype._set_data = function () {
            this._bake();
            this.vbo_position.set_size(this.V_position.length * 4);
            this.vbo_position.set_data(0, this.V_position);
            this.vbo_tangents.set_size(this.V_tangents.length * 4);
            this.vbo_tangents.set_data(0, this.V_tangents);
            this.vbo_angles.set_size(this.V_angles.length * 4);
            this.vbo_angles.set_data(0, this.V_angles);
            this.vbo_texcoord.set_size(this.V_texcoord.length * 4);
            this.vbo_texcoord.set_data(0, this.V_texcoord);
        };
        LineGLGlyph.prototype._set_visuals = function () {
            var _a;
            var color = color_1.color2rgba(this.glyph.visuals.line.line_color.value(), this.glyph.visuals.line.line_alpha.value());
            var cap = caps[this.glyph.visuals.line.line_cap.value()];
            var join = joins[this.glyph.visuals.line.line_join.value()];
            this.prog.set_uniform('u_color', 'vec4', color);
            this.prog.set_uniform('u_linewidth', 'float', [this.glyph.visuals.line.line_width.value()]);
            this.prog.set_uniform('u_antialias', 'float', [0.9]); // Smaller aa-region to obtain crisper images
            this.prog.set_uniform('u_linecaps', 'vec2', [cap, cap]);
            this.prog.set_uniform('u_linejoin', 'float', [join]);
            this.prog.set_uniform('u_miter_limit', 'float', [10.0]); // 10 should be a good value
            // https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-miterlimit
            var dash_pattern = this.glyph.visuals.line.line_dash.value();
            var dash_index = 0;
            var dash_period = 1;
            if (dash_pattern.length) {
                _a = this.dash_atlas.get_atlas_data(dash_pattern), dash_index = _a[0], dash_period = _a[1];
            }
            this.prog.set_uniform('u_dash_index', 'float', [dash_index]); // 0 means solid line
            this.prog.set_uniform('u_dash_phase', 'float', [this.glyph.visuals.line.line_dash_offset.value()]);
            this.prog.set_uniform('u_dash_period', 'float', [dash_period]);
            this.prog.set_uniform('u_dash_caps', 'vec2', [cap, cap]);
            this.prog.set_uniform('u_closed', 'float', [0]); // We dont do closed lines
        };
        LineGLGlyph.prototype._bake = function () {
            // This is what you get if you port 50 lines of numpy code to JS.
            // V_segment is handled in another method, because it depends on the aspect
            // ratio of the scale (The original paper/code assumed isotropic scaling).
            //
            // Buffer dtype from the Python implementation:
            //
            // self.vtype = np.dtype( [('a_position', 'f4', 2),
            //                         ('a_segment',  'f4', 2),
            //                         ('a_angles',   'f4', 2),
            //                         ('a_tangents', 'f4', 4),
            //                         ('a_texcoord', 'f4', 2) ])
            // Init array of implicit shape nx2
            var I, T, V_angles2, V_position2, V_tangents2, V_texcoord2, Vp, Vt;
            var n = this.nvertices;
            var _x = new Float64Array(this.glyph._x);
            var _y = new Float64Array(this.glyph._y);
            // Init vertex data
            var V_position = (Vp = new Float32Array(n * 2));
            //V_segment = new Float32Array(n*2)  # Done later
            var V_angles = new Float32Array(n * 2);
            var V_tangents = (Vt = new Float32Array(n * 4)); // mind the 4!
            // Position
            for (var i = 0, end = n; i < end; i++) {
                V_position[(i * 2) + 0] = _x[i] + this._baked_offset[0];
                V_position[(i * 2) + 1] = _y[i] + this._baked_offset[1];
            }
            // Tangents & norms (need tangents to calculate segments based on scale)
            this.tangents = (T = new Float32Array((n * 2) - 2));
            for (var i = 0, end = n - 1; i < end; i++) {
                T[(i * 2) + 0] = Vp[((i + 1) * 2) + 0] - Vp[(i * 2) + 0];
                T[(i * 2) + 1] = Vp[((i + 1) * 2) + 1] - Vp[(i * 2) + 1];
            }
            for (var i = 0, end = n - 1; i < end; i++) {
                // V['a_tangents'][+1:, :2] = T
                V_tangents[((i + 1) * 4) + 0] = T[(i * 2) + 0];
                V_tangents[((i + 1) * 4) + 1] = T[(i * 2) + 1];
                // V['a_tangents'][:-1, 2:] = T
                V_tangents[(i * 4) + 2] = T[(i * 2) + 0];
                V_tangents[(i * 4) + 3] = T[(i * 2) + 1];
            }
            // V['a_tangents'][0  , :2] = T[0]
            V_tangents[(0 * 4) + 0] = T[0];
            V_tangents[(0 * 4) + 1] = T[1];
            // V['a_tangents'][ -1, 2:] = T[-1]
            V_tangents[((n - 1) * 4) + 2] = T[((n - 2) * 2) + 0];
            V_tangents[((n - 1) * 4) + 3] = T[((n - 2) * 2) + 1];
            // Angles
            var A = new Float32Array(n);
            for (var i = 0, end = n; i < end; i++) {
                A[i] = Math.atan2((Vt[(i * 4) + 0] * Vt[(i * 4) + 3]) - (Vt[(i * 4) + 1] * Vt[(i * 4) + 2]), (Vt[(i * 4) + 0] * Vt[(i * 4) + 2]) + (Vt[(i * 4) + 1] * Vt[(i * 4) + 3]));
            }
            for (var i = 0, end = n - 1; i < end; i++) {
                V_angles[(i * 2) + 0] = A[i];
                V_angles[(i * 2) + 1] = A[i + 1];
            }
            // Step 1: A -- B -- C  =>  A -- B, B' -- C
            // Repeat our array 4 times
            var m = (4 * n) - 4;
            this.V_position = (V_position2 = new Float32Array(m * 2));
            this.V_angles = (V_angles2 = new Float32Array(m * 2));
            this.V_tangents = (V_tangents2 = new Float32Array(m * 4)); // mind the 4!
            this.V_texcoord = (V_texcoord2 = new Float32Array(m * 2));
            var o = 2;
            //
            // Arg, we really need an ndarray thing in JS :/
            for (var i = 0, end = n; i < end; i++) { // all nodes on the line
                for (var j = 0; j < 4; j++) { // the four quad vertices
                    for (var k = 0; k < 2; k++) { // xy
                        V_position2[((((i * 4) + j) - o) * 2) + k] = V_position[(i * 2) + k];
                        V_angles2[(((i * 4) + j) * 2) + k] = V_angles[(i * 2) + k];
                    } // no offset
                    for (var k = 0; k < 4; k++) {
                        V_tangents2[((((i * 4) + j) - o) * 4) + k] = V_tangents[(i * 4) + k];
                    }
                }
            }
            for (var i = 0, end = n; i < end; i++) {
                V_texcoord2[(((i * 4) + 0) * 2) + 0] = -1;
                V_texcoord2[(((i * 4) + 1) * 2) + 0] = -1;
                V_texcoord2[(((i * 4) + 2) * 2) + 0] = +1;
                V_texcoord2[(((i * 4) + 3) * 2) + 0] = +1;
                //
                V_texcoord2[(((i * 4) + 0) * 2) + 1] = -1;
                V_texcoord2[(((i * 4) + 1) * 2) + 1] = +1;
                V_texcoord2[(((i * 4) + 2) * 2) + 1] = -1;
                V_texcoord2[(((i * 4) + 3) * 2) + 1] = +1;
            }
            // Indices
            //I = np.resize( np.array([0,1,2,1,2,3], dtype=np.uint32), (n-1)*(2*3))
            //I += np.repeat( 4*np.arange(n-1), 6)
            var ni = (n - 1) * 6;
            this.I_triangles = (I = new Uint32Array(ni));
            // Order of indices is such that drawing as line_strip reveals the line skeleton
            // Might have implications on culling, if we ever turn that on.
            // Order in paper was: 0 1 2 1 2 3
            for (var i = 0, end = n; i < end; i++) {
                I[(i * 6) + 0] = 0 + (4 * i);
                I[(i * 6) + 1] = 1 + (4 * i);
                I[(i * 6) + 2] = 3 + (4 * i);
                I[(i * 6) + 3] = 2 + (4 * i);
                I[(i * 6) + 4] = 0 + (4 * i);
                I[(i * 6) + 5] = 3 + (4 * i);
            }
        };
        LineGLGlyph.prototype._update_scale = function (sx, sy) {
            // Update segment data and cumsum so the length along the line has the
            // scale aspect ratio in it. In the vertex shader we multiply with the
            // "isotropic part" of the scale.
            var V_segment2;
            var n = this.nvertices;
            var m = (4 * n) - 4;
            // Prepare arrays
            var T = this.tangents;
            var N = new Float32Array(n - 1);
            var V_segment = new Float32Array(n * 2); // Elements are initialized with 0
            this.V_segment = (V_segment2 = new Float32Array(m * 2));
            // Calculate vector lengths - with scale aspect ratio taken into account
            for (var i = 0, end = n - 1; i < end; i++) {
                N[i] = Math.sqrt(Math.pow((T[(i * 2) + 0] * sx), 2) + Math.pow((T[(i * 2) + 1] * sy), 2));
            }
            // Calculate Segments
            var cumsum = 0;
            for (var i = 0, end = n - 1; i < end; i++) {
                cumsum += N[i];
                V_segment[((i + 1) * 2) + 0] = cumsum;
                V_segment[(i * 2) + 1] = cumsum;
            }
            // Upscale (same loop as in _bake())
            for (var i = 0, end = n; i < end; i++) {
                for (var j = 0; j < 4; j++) {
                    for (var k = 0; k < 2; k++) {
                        V_segment2[(((i * 4) + j) * 2) + k] = V_segment[(i * 2) + k];
                    }
                }
            }
            // Update
            this.cumsum = cumsum; // L[-1] in Nico's code
            this.vbo_segment.set_size(this.V_segment.length * 4);
            this.vbo_segment.set_data(0, this.V_segment);
        };
        return LineGLGlyph;
    }(base_1.BaseGLGlyph));
    exports.LineGLGlyph = LineGLGlyph;
    LineGLGlyph.__name__ = "LineGLGlyph";
},
488: /* models/glyphs/webgl/utils/index.js */ function _(require, module, exports) {
    Object.defineProperty(exports, "__esModule", { value: true });
    var program_1 = require(489) /* ./program */;
    exports.Program = program_1.Program;
    var texture_1 = require(491) /* ./texture */;
    exports.Texture2d = texture_1.Texture2d;
    var buffer_1 = require(490) /* ./buffer */;
    exports.IndexBuffer = buffer_1.IndexBuffer;
    exports.VertexBuffer = buffer_1.VertexBuffer;
},
489: /* models/glyphs/webgl/utils/program.js */ function _(require, module, exports) {
    Object.defineProperty(exports, "__esModule", { value: true });
    var tslib_1 = require(1) /* tslib */;
    var buffer_1 = require(490) /* ./buffer */;
    var Program = /** @class */ (function () {
        function Program(gl) {
            this.gl = gl;
            this.UTYPEMAP = {
                float: "uniform1fv",
                vec2: "uniform2fv",
                vec3: "uniform3fv",
                vec4: "uniform4fv",
                int: "uniform1iv",
                ivec2: "uniform2iv",
                ivec3: "uniform3iv",
                ivec4: "uniform4iv",
                bool: "uniform1iv",
                bvec2: "uniform2iv",
                bvec3: "uniform3iv",
                bvec4: "uniform4iv",
                mat2: "uniformMatrix2fv",
                mat3: "uniformMatrix3fv",
                mat4: "uniformMatrix4fv",
                sampler1D: "uniform1i",
                sampler2D: "uniform1i",
                sampler3D: "uniform1i",
            };
            this.ATYPEMAP = {
                float: "vertexAttrib1f",
                vec2: "vertexAttrib2f",
                vec3: "vertexAttrib3f",
                vec4: "vertexAttrib4f",
            };
            this.ATYPEINFO = {
                float: [1, 5126],
                vec2: [2, 5126],
                vec3: [3, 5126],
                vec4: [4, 5126],
            };
            this._linked = false;
            this._validated = false;
            this._unset_variables = new Set();
            this._known_invalid = new Set();
            this._locations = new Map();
            this._samplers = new Map();
            this._attributes = new Map();
            this.handle = this.gl.createProgram();
        }
        Program.prototype.delete = function () {
            this.gl.deleteProgram(this.handle);
        };
        Program.prototype.activate = function () {
            this.gl.useProgram(this.handle);
        };
        Program.prototype.deactivate = function () {
            this.gl.useProgram(0);
        };
        Program.prototype.set_shaders = function (vert, frag) {
            // Set GLSL code for the vertex and fragment shader.
            //
            // This function takes care of setting the shading code and
            // compiling+linking it into a working program object that is ready
            // to use.
            //
            // Parameters
            // ----------
            // vert : str
            //     GLSL code for the vertex shader.
            // frag : str
            //     GLSL code for the fragment shader.
            var gl = this.gl;
            this._linked = false;
            var vert_handle = gl.createShader(gl.VERTEX_SHADER);
            var frag_handle = gl.createShader(gl.FRAGMENT_SHADER);
            var tmp = [
                [vert, vert_handle, "vertex"],
                [frag, frag_handle, "fragment"],
            ];
            for (var _i = 0, tmp_1 = tmp; _i < tmp_1.length; _i++) {
                var _b = tmp_1[_i], code = _b[0], handle = _b[1], type = _b[2];
                gl.shaderSource(handle, code);
                gl.compileShader(handle);
                var status = gl.getShaderParameter(handle, gl.COMPILE_STATUS);
                if (!status) {
                    var errors = gl.getShaderInfoLog(handle);
                    throw new Error("errors in " + type + " shader:\n" + errors);
                }
            }
            gl.attachShader(this.handle, vert_handle);
            gl.attachShader(this.handle, frag_handle);
            gl.linkProgram(this.handle);
            if (!gl.getProgramParameter(this.handle, gl.LINK_STATUS)) {
                var logs = gl.getProgramInfoLog(this.handle);
                throw new Error("Program link error:\n" + logs);
            }
            this._unset_variables = this._get_active_attributes_and_uniforms();
            gl.detachShader(this.handle, vert_handle);
            gl.detachShader(this.handle, frag_handle);
            gl.deleteShader(vert_handle);
            gl.deleteShader(frag_handle);
            this._known_invalid.clear();
            this._linked = true;
        };
        Program.prototype._get_active_attributes_and_uniforms = function () {
            // Retrieve active attributes and uniforms to be able to check that
            // all uniforms/attributes are set by the user.
            var gl = this.gl;
            this._locations.clear();
            var regex = new RegExp("(\\w+)\\s*(\\[(\\d+)\\])\\s*");
            var cu = gl.getProgramParameter(this.handle, gl.ACTIVE_UNIFORMS);
            var ca = gl.getProgramParameter(this.handle, gl.ACTIVE_ATTRIBUTES);
            var attributes = [];
            var uniforms = [];
            var stub5_seq = [
                [attributes, ca, gl.getActiveAttrib, gl.getAttribLocation],
                [uniforms, cu, gl.getActiveUniform, gl.getUniformLocation],
            ];
            for (var _i = 0, stub5_seq_1 = stub5_seq; _i < stub5_seq_1.length; _i++) {
                var _b = stub5_seq_1[_i], container = _b[0], count = _b[1], getActive = _b[2], getLocation = _b[3];
                for (var i = 0; i < count; i += 1) {
                    var info = getActive.call(gl, this.handle, i);
                    var name = info.name;
                    var m = name.match(regex);
                    if (m != null) {
                        var name_1 = m[1];
                        for (var j = 0; j < info.size; j += 1) {
                            container.push([name_1 + "[" + j + "]", info.type]);
                        }
                    }
                    else {
                        container.push([name, info.type]);
                    }
                    this._locations.set(name, getLocation.call(gl, this.handle, name));
                }
            }
            var attrs_and_uniforms = new Set();
            for (var _c = 0, attributes_1 = attributes; _c < attributes_1.length; _c++) {
                var name = attributes_1[_c][0];
                attrs_and_uniforms.add(name);
            }
            for (var _d = 0, uniforms_1 = uniforms; _d < uniforms_1.length; _d++) {
                var name = uniforms_1[_d][0];
                attrs_and_uniforms.add(name);
            }
            return attrs_and_uniforms;
        };
        Program.prototype.set_texture = function (name, value) {
            var _a;
            // Set a texture sampler.
            //
            // A texture is a 2 dimensional grid of colors/intensities that
            // can be applied to a face (or used for other means by providing
            // a regular grid of data).
            //
            // Parameters
            // ----------
            // name : str
            //     The name by which the texture is known in the GLSL code.
            // value : Texture2d
            //     The Texture2d object to bind.
            if (!this._linked) {
                throw new Error("Cannot set uniform when program has no code");
            }
            var handle = (_a = this._locations.get(name)) !== null && _a !== void 0 ? _a : -1;
            if (handle < 0) {
                if (!this._known_invalid.has(name)) {
                    this._known_invalid.add(name);
                    console.log("\"Variable " + name + " is not an active texture");
                }
                return;
            }
            if (this._unset_variables.has(name)) {
                this._unset_variables.delete(name);
            }
            this.activate();
            if (true) {
                var unit = this._samplers.size;
                if (this._samplers.has(name)) {
                    unit = this._samplers.get(name)[2];
                }
                this._samplers.set(name, [value._target, value.handle, unit]);
                this.gl.uniform1i(handle, unit);
            }
        };
        Program.prototype.set_uniform = function (name, type_, value) {
            var _a;
            // Set a uniform value.
            //
            // A uniform is a value that is global to both the vertex and
            // fragment shader.
            //
            // Parameters
            // ----------
            // name : str
            //     The name by which the uniform is known in the GLSL code.
            // type_ : str
            //     The type of the uniform, e.g. 'float', 'vec2', etc.
            // value : list of scalars
            //     The value for the uniform. Should be a list even for type float.
            if (!this._linked) {
                throw new Error("Cannot set uniform when program has no code");
            }
            var handle = (_a = this._locations.get(name)) !== null && _a !== void 0 ? _a : -1;
            if (handle < 0) {
                if (!this._known_invalid.has(name)) {
                    this._known_invalid.add(name);
                    console.log("Variable " + name + " is not an active uniform");
                }
                return;
            }
            if (this._unset_variables.has(name)) {
                this._unset_variables.delete(name);
            }
            var count = 1;
            if (!type_.startsWith("mat")) {
                var a_type = type_ == "int" || type_ == "bool" ? "float" : type_.replace(/^ib/, "");
                count = Math.floor(value.length / (this.ATYPEINFO[a_type][0]));
            }
            if (count > 1) {
                for (var j = 0; j < count; j += 1) {
                    if (this._unset_variables.has(name + "[" + j + "]")) {
                        var name_ = name + "[" + j + "]";
                        if (this._unset_variables.has(name_)) {
                            this._unset_variables.delete(name_);
                        }
                    }
                }
            }
            var funcname = this.UTYPEMAP[type_];
            this.activate();
            if (type_.startsWith("mat")) {
                this.gl[funcname](handle, false, value);
            }
            else {
                this.gl[funcname](handle, value);
            }
        };
        Program.prototype.set_attribute = function (name, type_, value, stride, offset) {
            if (stride === void 0) {
                stride = 0;
            }
            if (offset === void 0) {
                offset = 0;
            }
            var _a;
            // Set an attribute value.
            //
            // An attribute represents per-vertex data and can only be used
            // in the vertex shader.
            //
            // Parameters
            // ----------
            // name : str
            //     The name by which the attribute is known in the GLSL code.
            // type_ : str
            //     The type of the attribute, e.g. 'float', 'vec2', etc.
            // value : VertexBuffer, array
            //     If value is a VertexBuffer, it is used (with stride and offset)
            //     for the vertex data. If value is an array, its used to set
            //     the value of all vertices (similar to a uniform).
            // stide : int, default 0
            //     The stride to "sample" the vertex data inside the buffer. Unless
            //     multiple vertex data are packed into a single buffer, this should
            //     be zero.
            // offset : int, default 0
            //     The offset to "sample" the vertex data inside the buffer. Unless
            //     multiple vertex data are packed into a single buffer, or only
            //     a part of the data must be used, this should probably be zero.
            if (!this._linked) {
                throw new Error("Cannot set attribute when program has no code");
            }
            var handle = (_a = this._locations.get(name)) !== null && _a !== void 0 ? _a : -1;
            if (handle < 0) {
                if (!this._known_invalid.has(name)) {
                    this._known_invalid.add(name);
                    if (value instanceof buffer_1.VertexBuffer && offset > 0) {
                    }
                    else {
                        console.log("Variable " + name + " is not an active attribute");
                    }
                }
                return;
            }
            if (this._unset_variables.has(name)) {
                this._unset_variables.delete(name);
            }
            this.activate();
            if (!(value instanceof buffer_1.VertexBuffer)) {
                var funcname = this.ATYPEMAP[type_];
                this._attributes.set(name, [null, handle, funcname, value]);
            }
            else {
                var _b = this.ATYPEINFO[type_], size = _b[0], gtype = _b[1];
                var funcname = "vertexAttribPointer";
                var args = [size, gtype, false, stride, offset];
                this._attributes.set(name, [value.handle, handle, funcname, args]);
            }
        };
        Program.prototype._pre_draw = function () {
            this.activate();
            for (var _i = 0, _b = this._samplers.values(); _i < _b.length; _i++) {
                var _c = _b[_i], tex_target = _c[0], tex_handle = _c[1], unit = _c[2];
                this.gl.activeTexture(this.gl.TEXTURE0 + unit);
                this.gl.bindTexture(tex_target, tex_handle);
            }
            for (var _d = 0, _e = this._attributes.values(); _d < _e.length; _d++) {
                var _f = _e[_d], vbo_handle = _f[0], attr_handle = _f[1], funcname = _f[2], args = _f[3];
                if (vbo_handle != null) {
                    this.gl.bindBuffer(this.gl.ARRAY_BUFFER, vbo_handle);
                    this.gl.enableVertexAttribArray(attr_handle);
                    this.gl[funcname].apply(this.gl, tslib_1.__spreadArrays([attr_handle], args));
                }
                else {
                    this.gl.bindBuffer(this.gl.ARRAY_BUFFER, null);
                    this.gl.disableVertexAttribArray(attr_handle);
                    this.gl[funcname].apply(this.gl, tslib_1.__spreadArrays([attr_handle], args));
                }
            }
            if (!this._validated) {
                this._validated = true;
                this._validate();
            }
        };
        Program.prototype._validate = function () {
            if (this._unset_variables.size) {
                console.log("Program has unset variables: " + this._unset_variables);
            }
            this.gl.validateProgram(this.handle);
            if (!this.gl.getProgramParameter(this.handle, this.gl.VALIDATE_STATUS)) {
                console.log(this.gl.getProgramInfoLog(this.handle));
                throw new Error("Program validation error");
            }
        };
        Program.prototype.draw = function (mode, selection) {
            // Draw the current visualization defined by the program.
            //
            // Parameters
            // ----------
            // mode : GL enum
            //     Can be POINTS, LINES, LINE_LOOP, LINE_STRIP, LINE_FAN, TRIANGLES
            // selection : 2-element tuple or IndexBuffer
            //     The selection to draw, specified either as (first, count) or an
            //     IndexBuffer object.
            if (!this._linked) {
                throw new Error("Cannot draw program if code has not been set");
            }
            if (selection instanceof buffer_1.IndexBuffer) {
                this._pre_draw();
                selection.activate();
                var count = selection.buffer_size / 2;
                var gtype = this.gl.UNSIGNED_SHORT;
                this.gl.drawElements(mode, count, gtype, 0);
                selection.deactivate();
            }
            else {
                var first = selection[0], count = selection[1];
                if (count != 0) {
                    this._pre_draw();
                    this.gl.drawArrays(mode, first, count);
                }
            }
        };
        return Program;
    }());
    exports.Program = Program;
    Program.__name__ = "Program";
},
490: /* models/glyphs/webgl/utils/buffer.js */ function _(require, module, exports) {
    Object.defineProperty(exports, "__esModule", { value: true });
    var tslib_1 = require(1) /* tslib */;
    var Buffer = /** @class */ (function () {
        function Buffer(gl) {
            this.gl = gl;
            this._usage = 35048;
            this.buffer_size = 0;
            this.handle = this.gl.createBuffer();
        }
        Buffer.prototype.delete = function () {
            this.gl.deleteBuffer(this.handle);
        };
        Buffer.prototype.activate = function () {
            this.gl.bindBuffer(this._target, this.handle);
        };
        Buffer.prototype.deactivate = function () {
            this.gl.bindBuffer(this._target, null);
        };
        Buffer.prototype.set_size = function (nbytes) {
            // Set the size of the buffer in bytes.
            //
            // Parameters
            // ----------
            // nbytes : int
            //     The number of bytes that the buffer needs to hold.
            if (nbytes != this.buffer_size) {
                this.activate();
                this.gl.bufferData(this._target, nbytes, this._usage);
                this.buffer_size = nbytes;
            }
        };
        Buffer.prototype.set_data = function (offset, data) {
            // Set the buffer data.
            //
            // Parameters
            // ----------
            // offset : int
            //     The offset in bytes for the new data.
            // data : typed array
            //     The data to upload.
            this.activate();
            this.gl.bufferSubData(this._target, offset, data);
        };
        return Buffer;
    }());
    exports.Buffer = Buffer;
    Buffer.__name__ = "Buffer";
    var VertexBuffer = /** @class */ (function (_super) {
        tslib_1.__extends(VertexBuffer, _super);
        function VertexBuffer() {
            var _this = _super.apply(this, arguments) || this;
            _this._target = 34962;
            return _this;
        }
        return VertexBuffer;
    }(Buffer));
    exports.VertexBuffer = VertexBuffer;
    VertexBuffer.__name__ = "VertexBuffer";
    var IndexBuffer = /** @class */ (function (_super) {
        tslib_1.__extends(IndexBuffer, _super);
        function IndexBuffer() {
            var _this = _super.apply(this, arguments) || this;
            _this._target = 34963;
            return _this;
        }
        return IndexBuffer;
    }(Buffer));
    exports.IndexBuffer = IndexBuffer;
    IndexBuffer.__name__ = "IndexBuffer";
},
491: /* models/glyphs/webgl/utils/texture.js */ function _(require, module, exports) {
    Object.defineProperty(exports, "__esModule", { value: true });
    var assert_1 = require(122) /* ../../../../core/util/assert */;
    var Texture2d = /** @class */ (function () {
        function Texture2d(gl) {
            this.gl = gl;
            this._target = 3553;
            this._types = {
                Int8Array: 5120,
                Uint8Array: 5121,
                Int16Array: 5122,
                Uint16Array: 5123,
                Int32Array: 5124,
                Uint32Array: 5125,
                Float32Array: 5126,
            };
            this.handle = this.gl.createTexture();
        }
        Texture2d.prototype.delete = function () {
            this.gl.deleteTexture(this.handle);
        };
        Texture2d.prototype.activate = function () {
            this.gl.bindTexture(this._target, this.handle);
        };
        Texture2d.prototype.deactivate = function () {
            this.gl.bindTexture(this._target, 0);
        };
        Texture2d.prototype._get_alignment = function (width) {
            // Determines a textures byte alignment. If the width isn't a
            // power of 2 we need to adjust the byte alignment of the image.
            // The image height is unimportant.
            //
            // www.opengl.org/wiki/Common_Mistakes#Texture_upload_and_pixel_reads
            var alignments = [4, 8, 2, 1];
            for (var _i = 0, alignments_1 = alignments; _i < alignments_1.length; _i++) {
                var alignment = alignments_1[_i];
                if (width % alignment == 0) {
                    return alignment;
                }
            }
            assert_1.unreachable();
        };
        Texture2d.prototype.set_wrapping = function (wrap_s, wrap_t) {
            // Set the texture wrapping mode.
            //
            // Parameters
            // ----------
            // wrap_s : GL enum
            //     The mode to wrap the x dimension. Valid values are REPEAT
            //     CLAMP_TO_EDGE MIRRORED_REPEAT
            // wrap_t : GL enum
            //     The mode to wrap the y dimension. Same options as for wrap_s.
            this.activate();
            this.gl.texParameterf(this._target, this.gl.TEXTURE_WRAP_S, wrap_s);
            this.gl.texParameterf(this._target, this.gl.TEXTURE_WRAP_T, wrap_t);
        };
        Texture2d.prototype.set_interpolation = function (min, mag) {
            // Set the texture interpolation mode
            //
            // Parameters
            // ----------
            // min : GL enum
            //     The interpolation mode when minifying (i.e. zoomed out). Valid
            //     values are LINEAR and NEAREST.
            // max : GL enum
            //     The interpolation mode when magnifying (i.e. zoomed in). Valid
            //     values are LINEAR, NEAREST, NEAREST_MIPMAP_NEAREST,
            //     LINEAR_MIPMAP_NEAREST, NEAREST_MIPMAP_LINEAR, LINEAR_MIPMAP_LINEAR.
            this.activate();
            this.gl.texParameterf(this._target, this.gl.TEXTURE_MIN_FILTER, min);
            this.gl.texParameterf(this._target, this.gl.TEXTURE_MAG_FILTER, mag);
        };
        Texture2d.prototype.set_size = function (_d, format) {
            var width = _d[0], height = _d[1];
            var _a, _b, _c;
            // Set the size of the 2D texture.
            //
            // Parameters
            // ----------
            // shape : tuple of ints
            //     The shape of the data to upload
            // format : GL enum
            //     The format of the texture data. Can be LUMINANCE, LUMINANCE_ALPHA,
            //     RGB, and RGBA.
            if (width != ((_a = this._shape_format) === null || _a === void 0 ? void 0 : _a.width) || height != ((_b = this._shape_format) === null || _b === void 0 ? void 0 : _b.height) || format != ((_c = this._shape_format) === null || _c === void 0 ? void 0 : _c.format)) {
                this._shape_format = { width: width, height: height, format: format };
                this.activate();
                this.gl.texImage2D(this._target, 0, format, width, height, 0, format, this.gl.UNSIGNED_BYTE, null);
            }
        };
        Texture2d.prototype.set_data = function (offset, _d, data) {
            var width = _d[0], height = _d[1];
            // Set the 2D texture data.
            //
            // Parameters
            // ----------
            // offset : tuple of ints
            //     Offset in pixels for each dimension.
            // shape : tuple of ints
            //     The shape of the data to upload
            // data : typed array
            //     The actual pixel data. Can be of any type, but on the GPU the
            //     dat is stored in 8 bit precision.
            this.activate();
            var format = this._shape_format.format;
            var x = offset[0], y = offset[1];
            var gtype = this._types[data.constructor.name];
            if (gtype == null) {
                throw new Error("Type " + data.constructor.name + " not allowed for texture");
            }
            var alignment = this._get_alignment(width);
            if (alignment != 4) {
                this.gl.pixelStorei(this.gl.UNPACK_ALIGNMENT, alignment);
            }
            this.gl.texSubImage2D(this._target, 0, x, y, width, height, format, gtype, data);
            if (alignment != 4) {
                this.gl.pixelStorei(this.gl.UNPACK_ALIGNMENT, 4);
            }
        };
        return Texture2d;
    }());
    exports.Texture2d = Texture2d;
    Texture2d.__name__ = "Texture2d";
},
492: /* models/glyphs/webgl/base.js */ function _(require, module, exports) {
    Object.defineProperty(exports, "__esModule", { value: true });
    var color_1 = require(135) /* ../../../core/util/color */;
    var logging_1 = require(130) /* ../../../core/logging */;
    var BaseGLGlyph = /** @class */ (function () {
        function BaseGLGlyph(gl, glyph) {
            this.gl = gl;
            this.glyph = glyph;
            this.nvertices = 0;
            this.size_changed = false;
            this.data_changed = false;
            this.visuals_changed = false;
            this.init();
        }
        BaseGLGlyph.prototype.set_data_changed = function () {
            var data_size = this.glyph.data_size;
            if (data_size != this.nvertices) {
                this.nvertices = data_size;
                this.size_changed = true;
            }
            this.data_changed = true;
        };
        BaseGLGlyph.prototype.set_visuals_changed = function () {
            this.visuals_changed = true;
        };
        BaseGLGlyph.prototype.render = function (_ctx, indices, mainglyph) {
            var _a;
            if (indices.length == 0) {
                // Implementations assume at least one index to draw. We return true,
                // because there is no need to switch back to a fallback renderer.
                return true;
            }
            // Get transform
            var _b = [0, 1, 2], a = _b[0], b = _b[1], c = _b[2];
            var wx = 1; // Weights to scale our vectors
            var wy = 1;
            var _c = this.glyph.renderer.scope.map_to_screen([a * wx, b * wx, c * wx], [a * wy, b * wy, c * wy]), dx = _c[0], dy = _c[1];
            if (isNaN(dx[0] + dx[1] + dx[2] + dy[0] + dy[1] + dy[2])) {
                logging_1.logger.warn("WebGL backend (" + this.glyph.model.type + "): falling back to canvas rendering");
                return false;
            }
            // Try again, but with weighs so we're looking at ~100 in screen coordinates
            wx = 100 / Math.min(Math.max(Math.abs(dx[1] - dx[0]), 1e-12), 1e12);
            wy = 100 / Math.min(Math.max(Math.abs(dy[1] - dy[0]), 1e-12), 1e12);
            _a = this.glyph.renderer.scope.map_to_screen([a * wx, b * wx, c * wx], [a * wy, b * wy, c * wy]), dx = _a[0], dy = _a[1];
            // Test how linear it is
            if ((Math.abs((dx[1] - dx[0]) - (dx[2] - dx[1])) > 1e-6) ||
                (Math.abs((dy[1] - dy[0]) - (dy[2] - dy[1])) > 1e-6)) {
                logging_1.logger.warn("WebGL backend (" + this.glyph.model.type + "): falling back to canvas rendering");
                return false;
            }
            var _d = [(dx[1] - dx[0]) / wx, (dy[1] - dy[0]) / wy], sx = _d[0], sy = _d[1];
            var _e = this.glyph.renderer.plot_view.canvas_view.webgl.canvas, width = _e.width, height = _e.height;
            var trans = {
                pixel_ratio: this.glyph.renderer.plot_view.canvas_view.pixel_ratio,
                width: width, height: height,
                dx: dx[0] / sx, dy: dy[0] / sy, sx: sx, sy: sy,
            };
            this.draw(indices, mainglyph, trans);
            return true;
        };
        return BaseGLGlyph;
    }());
    exports.BaseGLGlyph = BaseGLGlyph;
    BaseGLGlyph.__name__ = "BaseGLGlyph";
    function line_width(width) {
        // Increase small values to make it more similar to canvas
        if (width < 2) {
            width = Math.sqrt(width * 2);
        }
        return width;
    }
    exports.line_width = line_width;
    function fill_array_with_vec(n, m, val) {
        var a = new Float32Array(n * m);
        for (var i = 0; i < n; i++) {
            for (var j = 0; j < m; j++) {
                a[i * m + j] = val[j];
            }
        }
        return a;
    }
    exports.fill_array_with_vec = fill_array_with_vec;
    function is_singular(visual, propname) {
        // This touches the internals of the visual, so we limit use in this function
        // See renderer.ts:cache_select() for similar code
        return visual[propname].spec.value !== undefined;
    }
    exports.is_singular = is_singular;
    function attach_float(prog, vbo, att_name, n, visual, name) {
        // Attach a float attribute to the program. Use singleton value if we can,
        // otherwise use VBO to apply array.
        if (!visual.doit) {
            vbo.used = false;
            prog.set_attribute(att_name, 'float', [0]);
        }
        else if (is_singular(visual, name)) {
            vbo.used = false;
            prog.set_attribute(att_name, 'float', [visual[name].value()]);
        }
        else {
            vbo.used = true;
            var a = new Float32Array(visual.get_array(name));
            vbo.set_size(n * 4);
            vbo.set_data(0, a);
            prog.set_attribute(att_name, 'float', vbo);
        }
    }
    exports.attach_float = attach_float;
    function attach_color(prog, vbo, att_name, n, visual, prefix) {
        // Attach the color attribute to the program. If there's just one color,
        // then use this single color for all vertices (no VBO). Otherwise we
        // create an array and upload that to the VBO, which we attahce to the prog.
        var rgba;
        var m = 4;
        var colorname = prefix + '_color';
        var alphaname = prefix + '_alpha';
        if (!visual.doit) {
            // Don't draw (draw transparent)
            vbo.used = false;
            prog.set_attribute(att_name, 'vec4', [0, 0, 0, 0]);
        }
        else if (is_singular(visual, colorname) && is_singular(visual, alphaname)) {
            // Nice and simple; both color and alpha are singular
            vbo.used = false;
            rgba = color_1.color2rgba(visual[colorname].value(), visual[alphaname].value());
            prog.set_attribute(att_name, 'vec4', rgba);
        }
        else {
            // Use vbo; we need an array for both the color and the alpha
            vbo.used = true;
            var colors = void 0;
            if (is_singular(visual, colorname)) {
                var val = color_1.encode_rgba(color_1.color2rgba(visual[colorname].value()));
                var array = new Uint32Array(n);
                array.fill(val);
                colors = array;
            }
            else
                colors = visual.get_array(colorname);
            var alphas = void 0;
            if (is_singular(visual, alphaname)) {
                var val = visual[alphaname].value();
                var array = new Float32Array(n);
                array.fill(val);
                alphas = array;
            }
            else
                alphas = visual.get_array(alphaname);
            // Create array of rgbs
            var a = new Float32Array(n * m);
            for (var i = 0, end = n; i < end; i++) {
                var rgba_1 = color_1.decode_rgba(colors[i]);
                if (rgba_1[3] == 1.0)
                    rgba_1[3] = alphas[i];
                a.set(rgba_1, i * m);
            }
            // Attach vbo
            vbo.set_size(n * m * 4);
            vbo.set_data(0, a);
            prog.set_attribute(att_name, 'vec4', vbo);
        }
    }
    exports.attach_color = attach_color;
},
493: /* models/glyphs/webgl/line.vert.js */ function _(require, module, exports) {
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.vertex_shader = "\nprecision mediump float;\n\nconst float PI = 3.14159265358979323846264;\nconst float THETA = 15.0 * 3.14159265358979323846264/180.0;\n\nuniform float u_pixel_ratio;\nuniform vec2 u_canvas_size, u_offset;\nuniform vec2 u_scale_aspect;\nuniform float u_scale_length;\n\nuniform vec4 u_color;\nuniform float u_antialias;\nuniform float u_length;\nuniform float u_linewidth;\nuniform float u_dash_index;\nuniform float u_closed;\n\nattribute vec2 a_position;\nattribute vec4 a_tangents;\nattribute vec2 a_segment;\nattribute vec2 a_angles;\nattribute vec2 a_texcoord;\n\nvarying vec4  v_color;\nvarying vec2  v_segment;\nvarying vec2  v_angles;\nvarying vec2  v_texcoord;\nvarying vec2  v_miter;\nvarying float v_length;\nvarying float v_linewidth;\n\nfloat cross(in vec2 v1, in vec2 v2)\n{\n    return v1.x*v2.y - v1.y*v2.x;\n}\n\nfloat signed_distance(in vec2 v1, in vec2 v2, in vec2 v3)\n{\n    return cross(v2-v1,v1-v3) / length(v2-v1);\n}\n\nvoid rotate( in vec2 v, in float alpha, out vec2 result )\n{\n    float c = cos(alpha);\n    float s = sin(alpha);\n    result = vec2( c*v.x - s*v.y,\n                   s*v.x + c*v.y );\n}\n\nvoid main()\n{\n    bool closed = (u_closed > 0.0);\n\n    // Attributes and uniforms to varyings\n    v_color = u_color;\n    v_linewidth = u_linewidth;\n    v_segment = a_segment * u_scale_length;\n    v_length = u_length * u_scale_length;\n\n    // Scale to map to pixel coordinates. The original algorithm from the paper\n    // assumed isotropic scale. We obviously do not have this.\n    vec2 abs_scale_aspect = abs(u_scale_aspect);\n    vec2 abs_scale = u_scale_length * abs_scale_aspect;\n\n    // Correct angles for aspect ratio\n    vec2 av;\n    av = vec2(1.0, tan(a_angles.x)) / abs_scale_aspect;\n    v_angles.x = atan(av.y, av.x);\n    av = vec2(1.0, tan(a_angles.y)) / abs_scale_aspect;\n    v_angles.y = atan(av.y, av.x);\n\n    // Thickness below 1 pixel are represented using a 1 pixel thickness\n    // and a modified alpha\n    v_color.a = min(v_linewidth, v_color.a);\n    v_linewidth = max(v_linewidth, 1.0);\n\n    // If color is fully transparent we just will discard the fragment anyway\n    if( v_color.a <= 0.0 ) {\n        gl_Position = vec4(0.0,0.0,0.0,1.0);\n        return;\n    }\n\n    // This is the actual half width of the line\n    float w = ceil(u_antialias+v_linewidth)/2.0;\n\n    vec2 position = (a_position + u_offset) * abs_scale;\n\n    vec2 t1 = normalize(a_tangents.xy * abs_scale_aspect);  // note the scaling for aspect ratio here\n    vec2 t2 = normalize(a_tangents.zw * abs_scale_aspect);\n    float u = a_texcoord.x;\n    float v = a_texcoord.y;\n    vec2 o1 = vec2( +t1.y, -t1.x);\n    vec2 o2 = vec2( +t2.y, -t2.x);\n\n    // This is a join\n    // ----------------------------------------------------------------\n    if( t1 != t2 ) {\n        float angle = atan (t1.x*t2.y-t1.y*t2.x, t1.x*t2.x+t1.y*t2.y);  // Angle needs recalculation for some reason\n        vec2 t  = normalize(t1+t2);\n        vec2 o  = vec2( + t.y, - t.x);\n\n        if ( u_dash_index > 0.0 )\n        {\n            // Broken angle\n            // ----------------------------------------------------------------\n            if( (abs(angle) > THETA) ) {\n                position += v * w * o / cos(angle/2.0);\n                float s = sign(angle);\n                if( angle < 0.0 ) {\n                    if( u == +1.0 ) {\n                        u = v_segment.y + v * w * tan(angle/2.0);\n                        if( v == 1.0 ) {\n                            position -= 2.0 * w * t1 / sin(angle);\n                            u -= 2.0 * w / sin(angle);\n                        }\n                    } else {\n                        u = v_segment.x - v * w * tan(angle/2.0);\n                        if( v == 1.0 ) {\n                            position += 2.0 * w * t2 / sin(angle);\n                            u += 2.0*w / sin(angle);\n                        }\n                    }\n                } else {\n                    if( u == +1.0 ) {\n                        u = v_segment.y + v * w * tan(angle/2.0);\n                        if( v == -1.0 ) {\n                            position += 2.0 * w * t1 / sin(angle);\n                            u += 2.0 * w / sin(angle);\n                        }\n                    } else {\n                        u = v_segment.x - v * w * tan(angle/2.0);\n                        if( v == -1.0 ) {\n                            position -= 2.0 * w * t2 / sin(angle);\n                            u -= 2.0*w / sin(angle);\n                        }\n                    }\n                }\n                // Continuous angle\n                // ------------------------------------------------------------\n            } else {\n                position += v * w * o / cos(angle/2.0);\n                if( u == +1.0 ) u = v_segment.y;\n                else            u = v_segment.x;\n            }\n        }\n\n        // Solid line\n        // --------------------------------------------------------------------\n        else\n        {\n            position.xy += v * w * o / cos(angle/2.0);\n            if( angle < 0.0 ) {\n                if( u == +1.0 ) {\n                    u = v_segment.y + v * w * tan(angle/2.0);\n                } else {\n                    u = v_segment.x - v * w * tan(angle/2.0);\n                }\n            } else {\n                if( u == +1.0 ) {\n                    u = v_segment.y + v * w * tan(angle/2.0);\n                } else {\n                    u = v_segment.x - v * w * tan(angle/2.0);\n                }\n            }\n        }\n\n    // This is a line start or end (t1 == t2)\n    // ------------------------------------------------------------------------\n    } else {\n        position += v * w * o1;\n        if( u == -1.0 ) {\n            u = v_segment.x - w;\n            position -= w * t1;\n        } else {\n            u = v_segment.y + w;\n            position += w * t2;\n        }\n    }\n\n    // Miter distance\n    // ------------------------------------------------------------------------\n    vec2 t;\n    vec2 curr = a_position * abs_scale;\n    if( a_texcoord.x < 0.0 ) {\n        vec2 next = curr + t2*(v_segment.y-v_segment.x);\n\n        rotate( t1, +v_angles.x/2.0, t);\n        v_miter.x = signed_distance(curr, curr+t, position);\n\n        rotate( t2, +v_angles.y/2.0, t);\n        v_miter.y = signed_distance(next, next+t, position);\n    } else {\n        vec2 prev = curr - t1*(v_segment.y-v_segment.x);\n\n        rotate( t1, -v_angles.x/2.0,t);\n        v_miter.x = signed_distance(prev, prev+t, position);\n\n        rotate( t2, -v_angles.y/2.0,t);\n        v_miter.y = signed_distance(curr, curr+t, position);\n    }\n\n    if (!closed && v_segment.x <= 0.0) {\n        v_miter.x = 1e10;\n    }\n    if (!closed && v_segment.y >= v_length)\n    {\n        v_miter.y = 1e10;\n    }\n\n    v_texcoord = vec2( u, v*w );\n\n    // Calculate position in device coordinates. Note that we\n    // already scaled with abs scale above.\n    vec2 normpos = position * sign(u_scale_aspect);\n    normpos += 0.5;  // make up for Bokeh's offset\n    normpos /= u_canvas_size / u_pixel_ratio;  // in 0..1\n    gl_Position = vec4(normpos*2.0-1.0, 0.0, 1.0);\n    gl_Position.y *= -1.0;\n}\n";
},
494: /* models/glyphs/webgl/line.frag.js */ function _(require, module, exports) {
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.fragment_shader = "\nprecision mediump float;\n\nconst float PI = 3.14159265358979323846264;\nconst float THETA = 15.0 * 3.14159265358979323846264/180.0;\n\nuniform sampler2D u_dash_atlas;\n\nuniform vec2 u_linecaps;\nuniform float u_miter_limit;\nuniform float u_linejoin;\nuniform float u_antialias;\nuniform float u_dash_phase;\nuniform float u_dash_period;\nuniform float u_dash_index;\nuniform vec2 u_dash_caps;\nuniform float u_closed;\n\nvarying vec4  v_color;\nvarying vec2  v_segment;\nvarying vec2  v_angles;\nvarying vec2  v_texcoord;\nvarying vec2  v_miter;\nvarying float v_length;\nvarying float v_linewidth;\n\n// Compute distance to cap ----------------------------------------------------\nfloat cap( int type, float dx, float dy, float t, float linewidth )\n{\n    float d = 0.0;\n    dx = abs(dx);\n    dy = abs(dy);\n    if      (type == 0)  discard;  // None\n    else if (type == 1)  d = sqrt(dx*dx+dy*dy);  // Round\n    else if (type == 3)  d = (dx+abs(dy));  // Triangle in\n    else if (type == 2)  d = max(abs(dy),(t+dx-abs(dy)));  // Triangle out\n    else if (type == 4)  d = max(dx,dy);  // Square\n    else if (type == 5)  d = max(dx+t,dy);  // Butt\n    return d;\n}\n\n// Compute distance to join -------------------------------------------------\nfloat join( in int type, in float d, in vec2 segment, in vec2 texcoord, in vec2 miter,\n           in float linewidth )\n{\n    // texcoord.x is distance from start\n    // texcoord.y is distance from centerline\n    // segment.x and y indicate the limits (as for texcoord.x) for this segment\n\n    float dx = texcoord.x;\n\n    // Round join\n    if( type == 1 ) {\n        if (dx < segment.x) {\n            d = max(d,length( texcoord - vec2(segment.x,0.0)));\n            //d = length( texcoord - vec2(segment.x,0.0));\n        } else if (dx > segment.y) {\n            d = max(d,length( texcoord - vec2(segment.y,0.0)));\n            //d = length( texcoord - vec2(segment.y,0.0));\n        }\n    }\n    // Bevel join\n    else if ( type == 2 ) {\n        if (dx < segment.x) {\n            vec2 x = texcoord - vec2(segment.x,0.0);\n            d = max(d, max(abs(x.x), abs(x.y)));\n\n        } else if (dx > segment.y) {\n            vec2 x = texcoord - vec2(segment.y,0.0);\n            d = max(d, max(abs(x.x), abs(x.y)));\n        }\n        /*  Original code for bevel which does not work for us\n        if( (dx < segment.x) ||  (dx > segment.y) )\n            d = max(d, min(abs(x.x),abs(x.y)));\n        */\n    }\n\n    return d;\n}\n\nvoid main()\n{\n    // If color is fully transparent we just discard the fragment\n    if( v_color.a <= 0.0 ) {\n        discard;\n    }\n\n    // Test if dash pattern is the solid one (0)\n    bool solid =  (u_dash_index == 0.0);\n\n    // Test if path is closed\n    bool closed = (u_closed > 0.0);\n\n    vec4 color = v_color;\n    float dx = v_texcoord.x;\n    float dy = v_texcoord.y;\n    float t = v_linewidth/2.0-u_antialias;\n    float width = 1.0;  //v_linewidth; original code had dashes scale with line width, we do not\n    float d = 0.0;\n\n    vec2 linecaps = u_linecaps;\n    vec2 dash_caps = u_dash_caps;\n    float line_start = 0.0;\n    float line_stop = v_length;\n\n    // Apply miter limit; fragments too far into the miter are simply discarded\n    if( (dx < v_segment.x) || (dx > v_segment.y) ) {\n        float into_miter = max(v_segment.x - dx, dx - v_segment.y);\n        if (into_miter > u_miter_limit*v_linewidth/2.0)\n          discard;\n    }\n\n    // Solid line --------------------------------------------------------------\n    if( solid ) {\n        d = abs(dy);\n        if( (!closed) && (dx < line_start) ) {\n            d = cap( int(u_linecaps.x), abs(dx), abs(dy), t, v_linewidth );\n        }\n        else if( (!closed) &&  (dx > line_stop) ) {\n            d = cap( int(u_linecaps.y), abs(dx)-line_stop, abs(dy), t, v_linewidth );\n        }\n        else {\n            d = join( int(u_linejoin), abs(dy), v_segment, v_texcoord, v_miter, v_linewidth );\n        }\n\n    // Dash line --------------------------------------------------------------\n    } else {\n        float segment_start = v_segment.x;\n        float segment_stop  = v_segment.y;\n        float segment_center= (segment_start+segment_stop)/2.0;\n        float freq          = u_dash_period*width;\n        float u = mod( dx + u_dash_phase*width, freq);\n        vec4 tex = texture2D(u_dash_atlas, vec2(u/freq, u_dash_index)) * 255.0 -10.0;  // conversion to int-like\n        float dash_center= tex.x * width;\n        float dash_type  = tex.y;\n        float _start = tex.z * width;\n        float _stop  = tex.a * width;\n        float dash_start = dx - u + _start;\n        float dash_stop  = dx - u + _stop;\n\n        // Compute extents of the first dash (the one relative to v_segment.x)\n        // Note: this could be computed in the vertex shader\n        if( (dash_stop < segment_start) && (dash_caps.x != 5.0) ) {\n            float u = mod(segment_start + u_dash_phase*width, freq);\n            vec4 tex = texture2D(u_dash_atlas, vec2(u/freq, u_dash_index)) * 255.0 -10.0;  // conversion to int-like\n            dash_center= tex.x * width;\n            //dash_type  = tex.y;\n            float _start = tex.z * width;\n            float _stop  = tex.a * width;\n            dash_start = segment_start - u + _start;\n            dash_stop = segment_start - u + _stop;\n        }\n\n        // Compute extents of the last dash (the one relatives to v_segment.y)\n        // Note: This could be computed in the vertex shader\n        else if( (dash_start > segment_stop)  && (dash_caps.y != 5.0) ) {\n            float u = mod(segment_stop + u_dash_phase*width, freq);\n            vec4 tex = texture2D(u_dash_atlas, vec2(u/freq, u_dash_index)) * 255.0 -10.0;  // conversion to int-like\n            dash_center= tex.x * width;\n            //dash_type  = tex.y;\n            float _start = tex.z * width;\n            float _stop  = tex.a * width;\n            dash_start = segment_stop - u + _start;\n            dash_stop  = segment_stop - u + _stop;\n        }\n\n        // This test if the we are dealing with a discontinuous angle\n        bool discontinuous = ((dx <  segment_center) && abs(v_angles.x) > THETA) ||\n                             ((dx >= segment_center) && abs(v_angles.y) > THETA);\n        //if( dx < line_start) discontinuous = false;\n        //if( dx > line_stop)  discontinuous = false;\n\n        float d_join = join( int(u_linejoin), abs(dy),\n                            v_segment, v_texcoord, v_miter, v_linewidth );\n\n        // When path is closed, we do not have room for linecaps, so we make room\n        // by shortening the total length\n        if (closed) {\n             line_start += v_linewidth/2.0;\n             line_stop  -= v_linewidth/2.0;\n        }\n\n        // We also need to take antialias area into account\n        //line_start += u_antialias;\n        //line_stop  -= u_antialias;\n\n        // Check is dash stop is before line start\n        if( dash_stop <= line_start ) {\n            discard;\n        }\n        // Check is dash start is beyond line stop\n        if( dash_start >= line_stop ) {\n            discard;\n        }\n\n        // Check if current dash start is beyond segment stop\n        if( discontinuous ) {\n            // Dash start is beyond segment, we discard\n            if( (dash_start > segment_stop) ) {\n                discard;\n                //gl_FragColor = vec4(1.0,0.0,0.0,.25); return;\n            }\n\n            // Dash stop is before segment, we discard\n            if( (dash_stop < segment_start) ) {\n                discard;  //gl_FragColor = vec4(0.0,1.0,0.0,.25); return;\n            }\n\n            // Special case for round caps (nicer with this)\n            if( dash_caps.x == 1.0 ) {\n                if( (u > _stop) && (dash_stop > segment_stop )  && (abs(v_angles.y) < PI/2.0)) {\n                    discard;\n                }\n            }\n\n            // Special case for round caps  (nicer with this)\n            if( dash_caps.y == 1.0 ) {\n                if( (u < _start) && (dash_start < segment_start )  && (abs(v_angles.x) < PI/2.0)) {\n                    discard;\n                }\n            }\n\n            // Special case for triangle caps (in & out) and square\n            // We make sure the cap stop at crossing frontier\n            if( (dash_caps.x != 1.0) && (dash_caps.x != 5.0) ) {\n                if( (dash_start < segment_start )  && (abs(v_angles.x) < PI/2.0) ) {\n                    float a = v_angles.x/2.0;\n                    float x = (segment_start-dx)*cos(a) - dy*sin(a);\n                    float y = (segment_start-dx)*sin(a) + dy*cos(a);\n                    if( x > 0.0 ) discard;\n                    // We transform the cap into square to avoid holes\n                    dash_caps.x = 4.0;\n                }\n            }\n\n            // Special case for triangle caps (in & out) and square\n            // We make sure the cap stop at crossing frontier\n            if( (dash_caps.y != 1.0) && (dash_caps.y != 5.0) ) {\n                if( (dash_stop > segment_stop )  && (abs(v_angles.y) < PI/2.0) ) {\n                    float a = v_angles.y/2.0;\n                    float x = (dx-segment_stop)*cos(a) - dy*sin(a);\n                    float y = (dx-segment_stop)*sin(a) + dy*cos(a);\n                    if( x > 0.0 ) discard;\n                    // We transform the caps into square to avoid holes\n                    dash_caps.y = 4.0;\n                }\n            }\n        }\n\n        // Line cap at start\n        if( (dx < line_start) && (dash_start < line_start) && (dash_stop > line_start) ) {\n            d = cap( int(linecaps.x), dx-line_start, dy, t, v_linewidth);\n        }\n        // Line cap at stop\n        else if( (dx > line_stop) && (dash_stop > line_stop) && (dash_start < line_stop) ) {\n            d = cap( int(linecaps.y), dx-line_stop, dy, t, v_linewidth);\n        }\n        // Dash cap left - dash_type = -1, 0 or 1, but there may be roundoff errors\n        else if( dash_type < -0.5 ) {\n            d = cap( int(dash_caps.y), abs(u-dash_center), dy, t, v_linewidth);\n            if( (dx > line_start) && (dx < line_stop) )\n                d = max(d,d_join);\n        }\n        // Dash cap right\n        else if( dash_type > 0.5 ) {\n            d = cap( int(dash_caps.x), abs(dash_center-u), dy, t, v_linewidth);\n            if( (dx > line_start) && (dx < line_stop) )\n                d = max(d,d_join);\n        }\n        // Dash body (plain)\n        else {// if( dash_type > -0.5 &&  dash_type < 0.5) {\n            d = abs(dy);\n        }\n\n        // Line join\n        if( (dx > line_start) && (dx < line_stop)) {\n            if( (dx <= segment_start) && (dash_start <= segment_start)\n                && (dash_stop >= segment_start) ) {\n                d = d_join;\n                // Antialias at outer border\n                float angle = PI/2.+v_angles.x;\n                float f = abs( (segment_start - dx)*cos(angle) - dy*sin(angle));\n                d = max(f,d);\n            }\n            else if( (dx > segment_stop) && (dash_start <= segment_stop)\n                     && (dash_stop >= segment_stop) ) {\n                d = d_join;\n                // Antialias at outer border\n                float angle = PI/2.+v_angles.y;\n                float f = abs((dx - segment_stop)*cos(angle) - dy*sin(angle));\n                d = max(f,d);\n            }\n            else if( dx < (segment_start - v_linewidth/2.)) {\n                discard;\n            }\n            else if( dx > (segment_stop + v_linewidth/2.)) {\n                discard;\n            }\n        }\n        else if( dx < (segment_start - v_linewidth/2.)) {\n            discard;\n        }\n        else if( dx > (segment_stop + v_linewidth/2.)) {\n            discard;\n        }\n    }\n\n    // Distance to border ------------------------------------------------------\n    d = d - t;\n    if( d < 0.0 ) {\n        gl_FragColor = color;\n    } else {\n        d /= u_antialias;\n        gl_FragColor = vec4(color.rgb, exp(-d*d)*color.a);\n    }\n}\n";
},
495: /* models/glyphs/webgl/markers.js */ function _(require, module, exports) {
    Object.defineProperty(exports, "__esModule", { value: true });
    var tslib_1 = require(1) /* tslib */;
    var utils_1 = require(488) /* ./utils */;
    var base_1 = require(492) /* ./base */;
    var markers_vert_1 = require(496) /* ./markers.vert */;
    var markers_frag_1 = require(497) /* ./markers.frag */;
    var circle_1 = require(327) /* ../circle */;
    var arrayable_1 = require(123) /* ../../../core/util/arrayable */;
    var logging_1 = require(130) /* ../../../core/logging */;
    // Base class for markers. All markers share the same GLSL, except for one
    // function that defines the marker geometry.
    var MarkerGLGlyph = /** @class */ (function (_super) {
        tslib_1.__extends(MarkerGLGlyph, _super);
        function MarkerGLGlyph() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        MarkerGLGlyph.prototype.init = function () {
            var gl = this.gl;
            var vert = markers_vert_1.vertex_shader;
            var frag = markers_frag_1.fragment_shader(this._marker_code);
            // The program
            this.prog = new utils_1.Program(gl);
            this.prog.set_shaders(vert, frag);
            // Real attributes
            this.vbo_x = new utils_1.VertexBuffer(gl);
            this.prog.set_attribute('a_x', 'float', this.vbo_x);
            this.vbo_y = new utils_1.VertexBuffer(gl);
            this.prog.set_attribute('a_y', 'float', this.vbo_y);
            this.vbo_s = new utils_1.VertexBuffer(gl);
            this.prog.set_attribute('a_size', 'float', this.vbo_s);
            this.vbo_a = new utils_1.VertexBuffer(gl);
            this.prog.set_attribute('a_angle', 'float', this.vbo_a);
            // VBO's for attributes (they may not be used if value is singleton)
            this.vbo_linewidth = new utils_1.VertexBuffer(gl);
            this.vbo_fg_color = new utils_1.VertexBuffer(gl);
            this.vbo_bg_color = new utils_1.VertexBuffer(gl);
            this.index_buffer = new utils_1.IndexBuffer(gl);
        };
        MarkerGLGlyph.prototype.draw = function (indices, mainGlyph, trans) {
            // The main glyph has the data, *this* glyph has the visuals.
            var mainGlGlyph = mainGlyph.glglyph;
            var nvertices = mainGlGlyph.nvertices;
            // Upload data if we must. Only happens for main glyph.
            if (mainGlGlyph.data_changed) {
                if (!(isFinite(trans.dx) && isFinite(trans.dy))) {
                    return; // not sure why, but it happens on init sometimes (#4367)
                }
                mainGlGlyph._baked_offset = [trans.dx, trans.dy]; // float32 precision workaround; used in _set_data() and below
                mainGlGlyph._set_data(nvertices);
                mainGlGlyph.data_changed = false;
            }
            else if (this.glyph instanceof circle_1.CircleView && this.glyph._radius != null &&
                (this.last_trans == null || trans.sx != this.last_trans.sx || trans.sy != this.last_trans.sy)) {
                // Keep screen radius up-to-date for circle glyph. Only happens when a radius is given
                this.last_trans = trans;
                this.vbo_s.set_data(0, new Float32Array(arrayable_1.map(this.glyph.sradius, function (s) { return s * 2; })));
            }
            // Update visuals if we must. Can happen for all glyphs.
            if (this.visuals_changed) {
                this._set_visuals(nvertices);
                this.visuals_changed = false;
            }
            // Handle transformation to device coordinates
            // Note the baked-in offset to avoid float32 precision problems
            var baked_offset = mainGlGlyph._baked_offset;
            this.prog.set_uniform('u_pixel_ratio', 'float', [trans.pixel_ratio]);
            this.prog.set_uniform('u_canvas_size', 'vec2', [trans.width, trans.height]);
            this.prog.set_uniform('u_offset', 'vec2', [trans.dx - baked_offset[0], trans.dy - baked_offset[1]]);
            this.prog.set_uniform('u_scale', 'vec2', [trans.sx, trans.sy]);
            // Select buffers from main glyph
            // (which may be this glyph but maybe not if this is a (non)selection glyph)
            this.prog.set_attribute('a_x', 'float', mainGlGlyph.vbo_x);
            this.prog.set_attribute('a_y', 'float', mainGlGlyph.vbo_y);
            this.prog.set_attribute('a_size', 'float', mainGlGlyph.vbo_s);
            this.prog.set_attribute('a_angle', 'float', mainGlGlyph.vbo_a);
            // Draw directly or using indices. Do not handle indices if they do not
            // fit in a uint16; WebGL 1.0 does not support uint32.
            if (indices.length == 0)
                return;
            else if (indices.length === nvertices)
                this.prog.draw(this.gl.POINTS, [0, nvertices]);
            else if (nvertices < 65535) {
                // On IE the marker size is reduced to 1 px when using an index buffer
                // A MS Edge dev on Twitter said on 24-04-2014: "gl_PointSize > 1.0 works
                // in DrawArrays; gl_PointSize > 1.0 in DrawElements is coming soon in the
                // next renderer update.
                var ua = window.navigator.userAgent;
                if ((ua.indexOf("MSIE ") + ua.indexOf("Trident/") + ua.indexOf("Edge/")) > 0) {
                    logging_1.logger.warn('WebGL warning: IE is known to produce 1px sprites whith selections.');
                }
                this.index_buffer.set_size(indices.length * 2);
                this.index_buffer.set_data(0, new Uint16Array(indices));
                this.prog.draw(this.gl.POINTS, this.index_buffer);
            }
            else {
                // Work around the limit that the indexbuffer must be uint16. We draw in chunks.
                // First collect indices in chunks
                var chunksize = 64000; // 65536
                var chunks = [];
                for (var i = 0, end = Math.ceil(nvertices / chunksize); i < end; i++) {
                    chunks.push([]);
                }
                for (var i = 0, end = indices.length; i < end; i++) {
                    var uint16_index = indices[i] % chunksize;
                    var chunk = Math.floor(indices[i] / chunksize);
                    chunks[chunk].push(uint16_index);
                }
                // Then draw each chunk
                for (var chunk = 0, end = chunks.length; chunk < end; chunk++) {
                    var these_indices = new Uint16Array(chunks[chunk]);
                    var offset = chunk * chunksize * 4;
                    if (these_indices.length === 0) {
                        continue;
                    }
                    this.prog.set_attribute('a_x', 'float', mainGlGlyph.vbo_x, 0, offset);
                    this.prog.set_attribute('a_y', 'float', mainGlGlyph.vbo_y, 0, offset);
                    this.prog.set_attribute('a_size', 'float', mainGlGlyph.vbo_s, 0, offset);
                    this.prog.set_attribute('a_angle', 'float', mainGlGlyph.vbo_a, 0, offset);
                    if (this.vbo_linewidth.used) {
                        this.prog.set_attribute('a_linewidth', 'float', this.vbo_linewidth, 0, offset);
                    }
                    if (this.vbo_fg_color.used) {
                        this.prog.set_attribute('a_fg_color', 'vec4', this.vbo_fg_color, 0, offset * 4);
                    }
                    if (this.vbo_bg_color.used) {
                        this.prog.set_attribute('a_bg_color', 'vec4', this.vbo_bg_color, 0, offset * 4);
                    }
                    // The actual drawing
                    this.index_buffer.set_size(these_indices.length * 2);
                    this.index_buffer.set_data(0, these_indices);
                    this.prog.draw(this.gl.POINTS, this.index_buffer);
                }
            }
        };
        MarkerGLGlyph.prototype._set_data = function (nvertices) {
            var n = nvertices * 4; // in bytes
            // Set buffer size
            this.vbo_x.set_size(n);
            this.vbo_y.set_size(n);
            this.vbo_a.set_size(n);
            this.vbo_s.set_size(n);
            // Upload data for x and y, apply a baked-in offset for float32 precision (issue #3795)
            // The exact value for the baked_offset does not matter, as long as it brings the data to less extreme values
            var xx = new Float64Array(this.glyph._x);
            var yy = new Float64Array(this.glyph._y);
            for (var i = 0, end = nvertices; i < end; i++) {
                xx[i] += this._baked_offset[0];
                yy[i] += this._baked_offset[1];
            }
            this.vbo_x.set_data(0, new Float32Array(xx));
            this.vbo_y.set_data(0, new Float32Array(yy));
            // Angle if available; circle does not have angle. If we don't set data, angle is default 0 in glsl
            if (this.glyph._angle != null) {
                this.vbo_a.set_data(0, new Float32Array(this.glyph._angle));
            }
            // Radius is special; some markers allow radius in data-coords instead of screen coords
            // @radius tells us that radius is in units, sradius is the pre-calculated screen radius
            if (this.glyph instanceof circle_1.CircleView && this.glyph._radius != null)
                this.vbo_s.set_data(0, new Float32Array(arrayable_1.map(this.glyph.sradius, function (s) { return s * 2; })));
            else
                this.vbo_s.set_data(0, new Float32Array(this.glyph._size));
        };
        MarkerGLGlyph.prototype._set_visuals = function (nvertices) {
            base_1.attach_float(this.prog, this.vbo_linewidth, 'a_linewidth', nvertices, this.glyph.visuals.line, 'line_width');
            base_1.attach_color(this.prog, this.vbo_fg_color, 'a_fg_color', nvertices, this.glyph.visuals.line, 'line');
            base_1.attach_color(this.prog, this.vbo_bg_color, 'a_bg_color', nvertices, this.glyph.visuals.fill, 'fill');
            // Static value for antialias. Smaller aa-region to obtain crisper images
            this.prog.set_uniform('u_antialias', 'float', [0.8]);
        };
        return MarkerGLGlyph;
    }(base_1.BaseGLGlyph));
    exports.MarkerGLGlyph = MarkerGLGlyph;
    MarkerGLGlyph.__name__ = "MarkerGLGlyph";
    function mk_marker(code) {
        return /** @class */ (function (_super) {
            tslib_1.__extends(class_1, _super);
            function class_1() {
                return _super !== null && _super.apply(this, arguments) || this;
            }
            Object.defineProperty(class_1.prototype, "_marker_code", {
                get: function () {
                    return code;
                },
                enumerable: true,
                configurable: true
            });
            return class_1;
        }(MarkerGLGlyph));
    }
    var glsl = tslib_1.__importStar(require(497) /* ./markers.frag */);
    exports.CircleGLGlyph = mk_marker(glsl.circle);
    exports.SquareGLGlyph = mk_marker(glsl.square);
    exports.DiamondGLGlyph = mk_marker(glsl.diamond);
    exports.TriangleGLGlyph = mk_marker(glsl.triangle);
    exports.InvertedTriangleGLGlyph = mk_marker(glsl.invertedtriangle);
    exports.HexGLGlyph = mk_marker(glsl.hex);
    exports.CrossGLGlyph = mk_marker(glsl.cross);
    exports.CircleCrossGLGlyph = mk_marker(glsl.circlecross);
    exports.SquareCrossGLGlyph = mk_marker(glsl.squarecross);
    exports.DiamondCrossGLGlyph = mk_marker(glsl.diamondcross);
    exports.XGLGlyph = mk_marker(glsl.x);
    exports.CircleXGLGlyph = mk_marker(glsl.circlex);
    exports.SquareXGLGlyph = mk_marker(glsl.squarex);
    exports.AsteriskGLGlyph = mk_marker(glsl.asterisk);
},
496: /* models/glyphs/webgl/markers.vert.js */ function _(require, module, exports) {
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.vertex_shader = "\nprecision mediump float;\nconst float SQRT_2 = 1.4142135623730951;\n//\nuniform float u_pixel_ratio;\nuniform vec2 u_canvas_size;\nuniform vec2 u_offset;\nuniform vec2 u_scale;\nuniform float u_antialias;\n//\nattribute float a_x;\nattribute float a_y;\nattribute float a_size;\nattribute float a_angle;  // in radians\nattribute float a_linewidth;\nattribute vec4  a_fg_color;\nattribute vec4  a_bg_color;\n//\nvarying float v_linewidth;\nvarying float v_size;\nvarying vec4  v_fg_color;\nvarying vec4  v_bg_color;\nvarying vec2  v_rotation;\n\nvoid main (void)\n{\n    v_size = a_size * u_pixel_ratio;\n    v_linewidth = a_linewidth * u_pixel_ratio;\n    v_fg_color = a_fg_color;\n    v_bg_color = a_bg_color;\n    v_rotation = vec2(cos(-a_angle), sin(-a_angle));\n    // Calculate position - the -0.5 is to correct for canvas origin\n    vec2 pos = (vec2(a_x, a_y) + u_offset) * u_scale; // in pixels\n    pos += 0.5;  // make up for Bokeh's offset\n    pos /= u_canvas_size / u_pixel_ratio;  // in 0..1\n    gl_Position = vec4(pos*2.0-1.0, 0.0, 1.0);\n    gl_Position.y *= -1.0;\n    gl_PointSize = SQRT_2 * v_size + 2.0 * (v_linewidth + 1.5*u_antialias);\n}\n";
},
497: /* models/glyphs/webgl/markers.frag.js */ function _(require, module, exports) {
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.fragment_shader = function (marker_code) { return "\nprecision mediump float;\nconst float SQRT_2 = 1.4142135623730951;\nconst float PI = 3.14159265358979323846264;\n//\nuniform float u_antialias;\n//\nvarying vec4  v_fg_color;\nvarying vec4  v_bg_color;\nvarying float v_linewidth;\nvarying float v_size;\nvarying vec2  v_rotation;\n\n" + marker_code + "\n\nvec4 outline(float distance, float linewidth, float antialias, vec4 fg_color, vec4 bg_color)\n{\n    vec4 frag_color;\n    float t = linewidth/2.0 - antialias;\n    float signed_distance = distance;\n    float border_distance = abs(signed_distance) - t;\n    float alpha = border_distance/antialias;\n    alpha = exp(-alpha*alpha);\n\n    // If fg alpha is zero, it probably means no outline. To avoid a dark outline\n    // shining through due to aa, we set the fg color to the bg color. Avoid if (i.e. branching).\n    float select = float(bool(fg_color.a));\n    fg_color.rgb = select * fg_color.rgb + (1.0  - select) * bg_color.rgb;\n    // Similarly, if we want a transparent bg\n    select = float(bool(bg_color.a));\n    bg_color.rgb = select * bg_color.rgb + (1.0  - select) * fg_color.rgb;\n\n    if( border_distance < 0.0)\n        frag_color = fg_color;\n    else if( signed_distance < 0.0 ) {\n        frag_color = mix(bg_color, fg_color, sqrt(alpha));\n    } else {\n        if( abs(signed_distance) < (linewidth/2.0 + antialias) ) {\n            frag_color = vec4(fg_color.rgb, fg_color.a * alpha);\n        } else {\n            discard;\n        }\n    }\n    return frag_color;\n}\n\nvoid main()\n{\n    vec2 P = gl_PointCoord.xy - vec2(0.5, 0.5);\n    P = vec2(v_rotation.x*P.x - v_rotation.y*P.y,\n             v_rotation.y*P.x + v_rotation.x*P.y);\n    float point_size = SQRT_2*v_size  + 2.0 * (v_linewidth + 1.5*u_antialias);\n    float distance = marker(P*point_size, v_size);\n    gl_FragColor = outline(distance, v_linewidth, u_antialias, v_fg_color, v_bg_color);\n    //gl_FragColor.rgb *= gl_FragColor.a;  // pre-multiply alpha\n}\n"; };
    exports.circle = "\nfloat marker(vec2 P, float size)\n{\n    return length(P) - size/2.0;\n}\n";
    exports.square = "\nfloat marker(vec2 P, float size)\n{\n    return max(abs(P.x), abs(P.y)) - size/2.0;\n}\n";
    exports.diamond = "\nfloat marker(vec2 P, float size)\n{\n    float x = SQRT_2 / 2.0 * (P.x * 1.5 - P.y);\n    float y = SQRT_2 / 2.0 * (P.x * 1.5 + P.y);\n    float r1 = max(abs(x), abs(y)) - size / (2.0 * SQRT_2);\n    return r1 / SQRT_2;\n}\n";
    exports.hex = "\nfloat marker(vec2 P, float size)\n{\n    vec2 q = abs(P);\n    return max(q.y * 0.57735 + q.x - 1.0 * size/2.0, q.y - 0.866 * size/2.0);\n}\n";
    exports.triangle = "\nfloat marker(vec2 P, float size)\n{\n    P.y -= size * 0.3;\n    float x = SQRT_2 / 2.0 * (P.x * 1.7 - P.y);\n    float y = SQRT_2 / 2.0 * (P.x * 1.7 + P.y);\n    float r1 = max(abs(x), abs(y)) - size / 1.6;\n    float r2 = P.y;\n    return max(r1 / SQRT_2, r2);  // Intersect diamond with rectangle\n}\n";
    exports.invertedtriangle = "\nfloat marker(vec2 P, float size)\n{\n    P.y += size * 0.3;\n    float x = SQRT_2 / 2.0 * (P.x * 1.7 - P.y);\n    float y = SQRT_2 / 2.0 * (P.x * 1.7 + P.y);\n    float r1 = max(abs(x), abs(y)) - size / 1.6;\n    float r2 = - P.y;\n    return max(r1 / SQRT_2, r2);  // Intersect diamond with rectangle\n}\n";
    exports.cross = "\nfloat marker(vec2 P, float size)\n{\n    float square = max(abs(P.x), abs(P.y)) - size / 2.5;   // 2.5 is a tweak\n    float cross = min(abs(P.x), abs(P.y)) - size / 100.0;  // bit of \"width\" for aa\n    return max(square, cross);\n}\n";
    exports.circlecross = "\nfloat marker(vec2 P, float size)\n{\n    // Define quadrants\n    float qs = size / 2.0;  // quadrant size\n    float s1 = max(abs(P.x - qs), abs(P.y - qs)) - qs;\n    float s2 = max(abs(P.x + qs), abs(P.y - qs)) - qs;\n    float s3 = max(abs(P.x - qs), abs(P.y + qs)) - qs;\n    float s4 = max(abs(P.x + qs), abs(P.y + qs)) - qs;\n    // Intersect main shape with quadrants (to form cross)\n    float circle = length(P) - size/2.0;\n    float c1 = max(circle, s1);\n    float c2 = max(circle, s2);\n    float c3 = max(circle, s3);\n    float c4 = max(circle, s4);\n    // Union\n    return min(min(min(c1, c2), c3), c4);\n}\n";
    exports.squarecross = "\nfloat marker(vec2 P, float size)\n{\n    // Define quadrants\n    float qs = size / 2.0;  // quadrant size\n    float s1 = max(abs(P.x - qs), abs(P.y - qs)) - qs;\n    float s2 = max(abs(P.x + qs), abs(P.y - qs)) - qs;\n    float s3 = max(abs(P.x - qs), abs(P.y + qs)) - qs;\n    float s4 = max(abs(P.x + qs), abs(P.y + qs)) - qs;\n    // Intersect main shape with quadrants (to form cross)\n    float square = max(abs(P.x), abs(P.y)) - size/2.0;\n    float c1 = max(square, s1);\n    float c2 = max(square, s2);\n    float c3 = max(square, s3);\n    float c4 = max(square, s4);\n    // Union\n    return min(min(min(c1, c2), c3), c4);\n}\n";
    exports.diamondcross = "\nfloat marker(vec2 P, float size)\n{\n    // Define quadrants\n    float qs = size / 2.0;  // quadrant size\n    float s1 = max(abs(P.x - qs), abs(P.y - qs)) - qs;\n    float s2 = max(abs(P.x + qs), abs(P.y - qs)) - qs;\n    float s3 = max(abs(P.x - qs), abs(P.y + qs)) - qs;\n    float s4 = max(abs(P.x + qs), abs(P.y + qs)) - qs;\n    // Intersect main shape with quadrants (to form cross)\n    float x = SQRT_2 / 2.0 * (P.x * 1.5 - P.y);\n    float y = SQRT_2 / 2.0 * (P.x * 1.5 + P.y);\n    float diamond = max(abs(x), abs(y)) - size / (2.0 * SQRT_2);\n    diamond /= SQRT_2;\n    float c1 = max(diamond, s1);\n    float c2 = max(diamond, s2);\n    float c3 = max(diamond, s3);\n    float c4 = max(diamond, s4);\n    // Union\n    return min(min(min(c1, c2), c3), c4);\n}\n";
    exports.x = "\nfloat marker(vec2 P, float size)\n{\n    float circle = length(P) - size / 1.6;\n    float X = min(abs(P.x - P.y), abs(P.x + P.y)) - size / 100.0;  // bit of \"width\" for aa\n    return max(circle, X);\n}\n";
    exports.circlex = "\nfloat marker(vec2 P, float size)\n{\n    float x = P.x - P.y;\n    float y = P.x + P.y;\n    // Define quadrants\n    float qs = size / 2.0;  // quadrant size\n    float s1 = max(abs(x - qs), abs(y - qs)) - qs;\n    float s2 = max(abs(x + qs), abs(y - qs)) - qs;\n    float s3 = max(abs(x - qs), abs(y + qs)) - qs;\n    float s4 = max(abs(x + qs), abs(y + qs)) - qs;\n    // Intersect main shape with quadrants (to form cross)\n    float circle = length(P) - size/2.0;\n    float c1 = max(circle, s1);\n    float c2 = max(circle, s2);\n    float c3 = max(circle, s3);\n    float c4 = max(circle, s4);\n    // Union\n    float almost = min(min(min(c1, c2), c3), c4);\n    // In this case, the X is also outside of the main shape\n    float Xmask = length(P) - size / 1.6;  // a circle\n    float X = min(abs(P.x - P.y), abs(P.x + P.y)) - size / 100.0;  // bit of \"width\" for aa\n    return min(max(X, Xmask), almost);\n}\n";
    exports.squarex = "\nfloat marker(vec2 P, float size)\n{\n    float x = P.x - P.y;\n    float y = P.x + P.y;\n    // Define quadrants\n    float qs = size / 2.0;  // quadrant size\n    float s1 = max(abs(x - qs), abs(y - qs)) - qs;\n    float s2 = max(abs(x + qs), abs(y - qs)) - qs;\n    float s3 = max(abs(x - qs), abs(y + qs)) - qs;\n    float s4 = max(abs(x + qs), abs(y + qs)) - qs;\n    // Intersect main shape with quadrants (to form cross)\n    float square = max(abs(P.x), abs(P.y)) - size/2.0;\n    float c1 = max(square, s1);\n    float c2 = max(square, s2);\n    float c3 = max(square, s3);\n    float c4 = max(square, s4);\n    // Union\n    return min(min(min(c1, c2), c3), c4);\n}\n";
    exports.asterisk = "\nfloat marker(vec2 P, float size)\n{\n    // Masks\n    float diamond = max(abs(SQRT_2 / 2.0 * (P.x - P.y)), abs(SQRT_2 / 2.0 * (P.x + P.y))) - size / (2.0 * SQRT_2);\n    float square = max(abs(P.x), abs(P.y)) - size / (2.0 * SQRT_2);\n    // Shapes\n    float X = min(abs(P.x - P.y), abs(P.x + P.y)) - size / 100.0;  // bit of \"width\" for aa\n    float cross = min(abs(P.x), abs(P.y)) - size / 100.0;  // bit of \"width\" for aa\n    // Result is union of masked shapes\n    return min(max(X, diamond), max(cross, square));\n}\n";
},
}, 485, {"models/glyphs/webgl/main":485,"models/glyphs/webgl/index":486,"models/glyphs/webgl/line":487,"models/glyphs/webgl/utils/index":488,"models/glyphs/webgl/utils/program":489,"models/glyphs/webgl/utils/buffer":490,"models/glyphs/webgl/utils/texture":491,"models/glyphs/webgl/base":492,"models/glyphs/webgl/line.vert":493,"models/glyphs/webgl/line.frag":494,"models/glyphs/webgl/markers":495,"models/glyphs/webgl/markers.vert":496,"models/glyphs/webgl/markers.frag":497}, {});
})

//# sourceMappingURL=bokeh-gl.legacy.js.map
