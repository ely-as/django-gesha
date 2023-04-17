const { dest, series } = require("gulp");
const browserify = require("browserify");
const buffer = require("vinyl-buffer");
const fancy_log = require("fancy-log");
const source = require("vinyl-source-stream");
const sourcemaps = require("gulp-sourcemaps");
const terser = require("gulp-terser");
const tsify = require("tsify");
const watchify = require("watchify");

require('dotenv').config();

const debug = (String(process.env.DEBUG).toLowerCase() === "true");
const paths = {
  entries: ["js_src/main.ts"],
  dest: "gesha/static/gesha/dist/js",
  outfile: "django-gesha.bundle.min.js"
};

var browserifyObj = browserify({
  basedir: ".",
  debug: debug,
  entries: paths.entries,
  cache: {},
  packageCache: {},
}).plugin(tsify)

function bundle(cb) {
  return browserifyObj
    .bundle()
    .on("error", fancy_log)
    .pipe(source(paths.outfile))
    .pipe(buffer())
    .pipe(sourcemaps.init({ loadMaps: true }))
    .pipe(terser({
      mangle: true
    }))
    .pipe(sourcemaps.write("./"))
    .pipe(dest(paths.dest));
}

function watch(cb) {
  var watchedBrowserify = watchify(browserifyObj);
  bundle();
  watchedBrowserify.on("update", bundle);
  watchedBrowserify.on("log", fancy_log);
}

exports.build = bundle;
exports.default = exports.build;
exports.watch = watch;
