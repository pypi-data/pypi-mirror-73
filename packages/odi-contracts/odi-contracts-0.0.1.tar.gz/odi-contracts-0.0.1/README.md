# ODIContracts

ODIContracts implements IRC2 standard token which is equivalent to [ERC20]() for [ICON](https://icon.foundation/?lang=en) blockchain. It helps to keep track of [fungible](https://en.wikipedia.org/wiki/Fungibility) tokens.

There are a few core contracts to implement IRC2 token.

-   [IIRC2](): Interface IRC2 methods should confirm into.
-   [IRC2](IRC2.md): The base implementation of IRC2 contract.

This has been extended to implement the following.

-   [IRC2Mintable](IRC2Mintable.md): To create token supply.
-   [IRC2Capped](IRC2Capped.md): Total supply cannot exceed the cap amount.
-   [IRC2Burnable](IRC2Burnable.md): To destroy the tokens.
-   [IRC2Pausable](IRC2Pausable.md): To pause token operation for all users.
