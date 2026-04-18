{
  description = "hackathon visualizer";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }:
  let
    pkgs = import nixpkgs { system = "x86_64-linux"; };
  in {
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
