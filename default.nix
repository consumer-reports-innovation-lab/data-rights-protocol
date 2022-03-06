# ref https://github.com/nix-community/poetry2nix/issues/423
{ pkgs ? import <nixpkgs> {}, poetry2nix ? pkgs.poetry2nix, stdenv ? pkgs.stdenv }:
let 
  mkPoetryApplication' = { projectDir, editablePackageSources, overrides ? poetry2nix.defaultPoetryOverrides, ... }@args:
    let
      # pass all args which are not specific to mkPoetryEnv
      app = poetry2nix.mkPoetryApplication (builtins.removeAttrs args [ "editablePackageSources" ]);

      # pass args specific to mkPoetryEnv and all remaining arguments to mkDerivation
      editableEnv = stdenv.mkDerivation (
        {
          name = "editable-env";
          src = poetry2nix.mkPoetryEnv {
            inherit projectDir editablePackageSources overrides;
          };

          # copy all the output of mkPoetryEnv so that patching and wrapping of outputs works
          installPhase = ''
        mkdir -p $out
        cp -a * $out
      '';
        } // builtins.removeAttrs args [ "projectDir" "editablePackageSources" "overrides" ]
      );
    in 
      app.overrideAttrs (super: {
        passthru = super.passthru // { inherit editableEnv; };
      });
in mkPoetryApplication' {
  projectDir = ./.;
  overrides = pkgs.poetry2nix.overrides.withDefaults (self: super: {
    typing-extensions = super.typing-extensions.overridePythonAttrs(old: {
      format = "flit";
    });
  });
  editablePackageSources = {
    datarightsprotocol = ./src;
  };
}
