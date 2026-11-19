{
  description = "Terraform Infrastructure Flake";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    # Release notes and versions for `just release`.
    vesnik = {
      url = "github:nklmilojevic/vesnik/v0.2.0";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, vesnik }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { system = system; config.allowUnfree = true; };
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            pkgs.go-task
            pkgs.gitleaks
          ];

          packages = [ pkgs.lefthook pkgs.terraform pkgs.git-secrets pkgs.just vesnik.packages.${system}.default ];
        };
      });
}
