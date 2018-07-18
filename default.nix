with import <nixpkgs> {};
with python3Packages;

buildPythonApplication {
  name = "srkwarrior";
  src = lib.cleanSource ./.;

  propagatedBuildInputs = [ bugwarrior ];

  HOME = ".";
}
