{ pkgs ? import <nixpkgs> {} }:

let
  myAppEnv = (import ./default.nix {}).dependencyEnv;
in pkgs.mkShell {
  packages = [
    myAppEnv
    pkgs.poetry
  ];
}
