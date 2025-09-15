#eval False → True

example (P Q : Prop) (h : P → Q) (hp : P) : Q := by
  apply h
  apply hp


example (P Q : Prop) (hq : Q) : P → Q := by
  intro hp
  apply hq


#eval ¬ True

example (P Q: Prop) (h1 : P → Q) (h2 : Q → P) : P ↔ Q := by
  constructor
  · apply h1
  · apply h2


example (P Q : Prop) (hq : Q) : (Q → P) ↔ P := by
  constructor

  case mp =>
    intro h
    exact h hq

  case mpr =>
    intro hp hq
    exact hp


  example (P Q : Prop): (¬ P ∨ Q) → (P → Q) := by
    intro h
    intro hp
    cases h with
    | inl hn =>
      exfalso
      apply hn
      exact hp
    | inr hq =>
      exact hq


  example (P Q : Prop) : ¬ (P ∨ Q) ↔ ¬ P ∧ ¬ Q := by
    constructor <;> intro h1
    · constructor <;> intro h2 --# ¬ P ∧ ¬ Q のゴールを分割
      · apply h1 -- ここでは h1 : ¬ (P ∨ Q) で、 h2: Pになってる
        left --
        assumption
      · apply h1
        right
        assumption
    · intro hpq
      cases hpq with
      | inl hp =>
        apply h1.left
        assumption
      | inr hq =>
        apply h1.right
        assumption

example (P : Prop) : ¬¬¬ P → ¬ P := by
  intro h3np hp

  have : ¬¬ P := by
    intro hnp
    contradiction

  contradiction

example (P : Prop) : ¬ (P ↔ ¬P) := by
  intro h
  exfalso

  have nP: ¬ P := by
    intro p
    exact (h.mp p) p

  have p' : P := by
    exact h.mpr nP

  contradiction
