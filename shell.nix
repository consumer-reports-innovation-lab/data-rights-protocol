{ pkgs ? import <nixpkgs> {} }:

let
  myAppEnv = pkgs.poetry2nix.mkPoetryEnv {
    projectDir = ./.;
    overrides = pkgs.poetry2nix.overrides.withDefaults (self: super: {
      typing-extensions = super.typing-extensions.overridePythonAttrs(old: {
        format = "flit";
      });
    });
  };
in pkgs.mkShell {
  packages = [
    myAppEnv
    pkgs.poetry
  ];
}
