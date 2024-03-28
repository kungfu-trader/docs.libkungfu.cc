const fs = require("fs");
const path = require("path");
const os = require("os");
const semver = require("semver");
const sywac = require("./sywac");
const { run } = require("./run");

sywac(module, (cli) => {
  cli
    .command("build", () => {
      const docsDir = path.resolve("docs");
      const latexDir = path.resolve("build", "latex");
      const stageDir = path.resolve("build", "stage", "kungfu");

      process.env.PYTHONPATH = path.resolve("src", "python");

      const getPackageJsonPath = (p) =>
        path.resolve(docsDir, p, "package.json");
      const buildDoc = (label) => (p) => {
        const packageJson = JSON.parse(fs.readFileSync(getPackageJsonPath(p)));
        const kungfuVersion = semver.parse(
          packageJson.kungfuVersion ||
            packageJson.dependencies["@kungfu-trader/kungfu-core"]
        );
        const docVersion = semver.coerce(kungfuVersion);
        const docVersionLabel = `v${docVersion.major}.${docVersion.minor}`;
        const sourceDir = path.resolve(docsDir, p, "src");
        const latexOutputDir = path.resolve(latexDir, label || docVersionLabel);
        const outputDir = path.resolve(stageDir, label || docVersionLabel);
        // run("poetry", [
        //   "run",
        //   "sphinx-build",
        //   "-M",
        //   "latexpdf",
        //   sourceDir,
        //   latexOutputDir,
        // ]);
        run("poetry", ["run", "sphinx-build", sourceDir, outputDir]);
        // fs.copyFileSync(
        //   path.join(latexOutputDir, "latex", "index.pdf"),
        //   path.join(outputDir, `Kungfu-Doc-${label || docVersionLabel}.pdf`)
        // );
        return {
          dir: p,
          version: kungfuVersion,
        };
      };

      const compareVersion = (a, b) => semver.compare(a.version, b.version);

      const docs = fs
        .readdirSync("docs")
        .filter((p) => {
          const moduleDir = path.join(docsDir, p);
          return (
            fs.lstatSync(moduleDir).isDirectory() &&
            fs.existsSync(getPackageJsonPath(p))
          );
        })
        .map(buildDoc())
        .sort(compareVersion);

      const latestDoc = docs.filter((p) => !p.version.prerelease.length).pop();
      const prerelaseDoc = docs
        .filter((p) => p.version.prerelease.length)
        .pop();

      process.env.KUNGFU_DOC_HAS_PRERELEASE = prerelaseDoc ? "true" : "false";

      latestDoc && buildDoc("latest")(latestDoc.dir);
      prerelaseDoc && buildDoc("prerelease")(prerelaseDoc.dir);

      const redirectHtmlPath = path.resolve(stageDir, "redirect.html");
      const latestIndexURI = "latest/index.html";
      fs.writeFileSync(
        redirectHtmlPath,
        `<head><meta http-equiv="refresh" content="3; URL=${latestIndexURI}"/></head>` +
          os.EOL +
          "<body>" +
          os.EOL +
          '<div style="text-align:center;">' +
          os.EOL +
          '<img style="display:block;margin:auto;width:50%;" src="latest/_static/images/banner.jpg">' +
          os.EOL +
          `<strong>Redirecting to <a href="${latestIndexURI}">latest released version</a></strong>` +
          os.EOL +
          "</div>" +
          os.EOL +
          "</body>" +
          os.EOL
      );
    })
    .command("clean", () => {
      fs.rmSync("build", {
        recursive: true,
        force: true,
      });
    });
});
