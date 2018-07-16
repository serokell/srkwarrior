with import <nixpkgs> {};
with python3Packages;

buildPythonApplication {
  name = "serokellwarrior";
  src = lib.cleanSource ./.;

  propagatedBuildInputs = [ bugwarrior ];

  HOME = ".";
}
