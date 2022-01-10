{ pkgs ? import <nixpkgs> {} }:

let
  myAppEnv = pkgs.poetry2nix.mkPoetryEnv {
    projectDir = ./.;
    # overrides = import ./poetry-overrides.nix { inherit pkgs; };
    overrides = pkgs.poetry2nix.overrides.withDefaults (self: super: {
      typing-extensions = super.typing-extensions.overridePythonAttrs(old: {
        format = "flit";
      });
    });
  };
in pkgs.mkShell {
  packages = [
    myAppEnv
    pkgs.pandoc
    pkgs.poetry
    # inotify-tools
  ];
}
