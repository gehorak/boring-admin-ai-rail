# Example Architecture Canon: Lantern Notes

## Canonical Boundaries

- the interface layer accepts user input and presents results;
- the application layer owns note use cases;
- the storage layer owns persistence details.

## Dependency Rules

- interfaces may call application use cases;
- application use cases may call the storage boundary;
- storage details must not leak into the interface layer.

## Approved Patterns

- one named use case per user-visible workflow;
- validation at the boundary before persistence.

## Forbidden Patterns

- direct persistence calls from interface code;
- hidden side effects in read-only review flows.
