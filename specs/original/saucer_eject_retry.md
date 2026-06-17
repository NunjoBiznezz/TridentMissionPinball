# Saucer Eject Behavior

Status: APPROVED

## Behavior

When a ball enters the saucer, the machine kicks it back to the playfield.
Ejection is not considered complete until the ball has physically left the
saucer. If the ball fails to leave, the machine kicks again. After three
failed attempts the machine raises a stuck-ball condition.

The saucer never fire-and-forgets: a kick that does not result in the ball
leaving is always retried.
