with import <nixpkgs> {};
with python3Packages;

buildPythonApplication {
  name = "serokellwarrior";
  propagatedBuildInputs = [ bugwarrior ];
  src = lib.cleanSource ./.;

  HOME = ".";
}
