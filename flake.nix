{
  description = "hackathon visualizer";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }:
  let
    pkgs = import nixpkgs { system = "x86_64-linux"; };
  in {
    packages.x86_64-linux.default = pkgs.python3Packages.buildPythonApplication {
     pname = "audioviz"; 
     version = "0.1";
     propagatedBuildInputs = with pkgs.python3Packages; [
       soundcard
       pyqt6
       pyopengl
       scipy
     ];
     src = ./.;
     pyproject = true;
     build-system = with pkgs.python3Packages; [ setuptools ];
    };
    devShells.x86_64-linux.default = pkgs.mkShell {
      name = "audioviz";
      packages = with pkgs.python3Packages; [
        soundcard
        pyqt6
        pyopengl
        scipy
      ];
    };
  };
}
