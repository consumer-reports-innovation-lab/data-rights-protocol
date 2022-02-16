{ pkgs ? import <nixpkgs> {} }:

pkgs.poetry2nix.mkPoetryApplication {
  projectDir = ./.;
  overrides = pkgs.poetry2nix.overrides.withDefaults (self: super: {
    typing-extensions = super.typing-extensions.overridePythonAttrs(old: {
      format = "flit";
    });
  });
}
