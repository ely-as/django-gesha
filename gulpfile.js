const gulp = require("gulp");
const browserify = require("browserify");
const buffer = require("vinyl-buffer");
const cleanCSS = require('gulp-clean-css');
const fancy_log = require("fancy-log");
const rename = require("gulp-rename");
const source = require("vinyl-source-stream");
const sourcemaps = require("gulp-sourcemaps");
const terser = require("gulp-terser");
const ts = require('gulp-typescript');
const tsify = require("tsify");
const watchify = require("watchify");

require('dotenv').config();

const debug = (String(process.env.DEBUG).toLowerCase() === "true");
const paths = {
  bundle: {
    entries: ["js_src/main.ts"],
    dest: "gesha/static/gesha/dist/js",
    outfile: "django-gesha.bundle.min.js"
  },
  types: {
    dest: "js_dist"
  },
  docs_styles: {
    src: ["docs/stylesheets/extra.css"],
    dest: "docs/stylesheets/"
  }
};
const tsProject = ts.createProject("tsconfig.json");

var browserifyObj = browserify({
  basedir: ".",
  debug: debug,
  entries: paths.bundle.entries,
  cache: {},
  packageCache: {},
}).plugin(tsify)

function bundle() {
  return browserifyObj
    .bundle()
    .on("error", fancy_log)
    .pipe(source(paths.bundle.outfile))
    .pipe(buffer())
    .pipe(sourcemaps.init({ loadMaps: true }))
    .pipe(terser({
      mangle: true
    }))
    .pipe(sourcemaps.write("./"))
    .pipe(gulp.dest(paths.bundle.dest));
}

async function clean() {
  const { deleteAsync } = await import("del");
  await deleteAsync(paths.types.dest);
}

function types() {
  return tsProject.src()
    .pipe(sourcemaps.init())
    .pipe(ts({
      declaration: true,
      emitDeclarationOnly: true
    }))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(paths.types.dest));
}

function docs_styles() {
  return gulp.src(paths.docs_styles.src, { sourcemaps: true })
    .pipe(cleanCSS())
    .pipe(rename({ suffix: ".min" }))
    .pipe(gulp.dest(paths.docs_styles.dest));
}

const build = gulp.parallel(bundle, gulp.series(clean, types));

function watch() {
  var watchedBrowserify = watchify(browserifyObj);
  build();
  watchedBrowserify.on("update", build);
  watchedBrowserify.on("log", fancy_log);
  gulp.watch(paths.docs_styles.src, docs_styles);
}

exports.build = build;
exports.clean = clean;
exports.default = gulp.parallel(build, docs_styles);
exports.docs_styles = docs_styles;
exports.types = types;
exports.watch = watch;
