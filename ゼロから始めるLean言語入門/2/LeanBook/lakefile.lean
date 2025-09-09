import Lake
open Lake DSL

package "LeanBook" where
  version := v!"0.1.0"

@[default_target]
lean_lib «LeanBook» where
  -- add library configuration options here
  globs := #[.submodules `LeanBook]
