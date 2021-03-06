[![Build Status](https://app.travis-ci.com/Swivel-Finance/swivel-py.svg?token=mHzJQzb11WHSPwztZw8B&branch=main)](https://app.travis-ci.com/Swivel-Finance/swivel-py)
### A python library for interaction with the Swivel protocol
```
 ________  ___       __   ___  ___      ___ _______   ___           ________  ___    ___ 
|\   ____\|\  \     |\  \|\  \|\  \    /  /|\  ___ \ |\  \         |\   __  \|\  \  /  /|
\ \  \___|\ \  \    \ \  \ \  \ \  \  /  / | \   __/|\ \  \        \ \  \|\  \ \  \/  / /
 \ \_____  \ \  \  __\ \  \ \  \ \  \/  / / \ \  \_|/_\ \  \        \ \   ____\ \    / / 
  \|____|\  \ \  \|\__\_\  \ \  \ \    / /   \ \  \_|\ \ \  \____  __\ \  \___|\/  /  /  
    ____\_\  \ \____________\ \__\ \__/ /     \ \_______\ \_______\\__\ \__\ __/  / /    
   |\_________\|____________|\|__|\|__|/       \|_______|\|_______\|__|\|__||\___/ /     
   \|_________|                                                             \|___|/      
```
### About
Swivel.py is a collection of what we call *Higher Order Contracts*. These are language specific, Python in this case,
constructs that abstract and encapsulate the tedious and boilerplate logic of working with low-level smart contracts.

## Installation

    pip install -r requirements.txt

## Running Tests

    pytest
    
### Examples
Before we dive into the specifics, you should take a look at the classes in action. There is an entire [repo](https://github.com/Swivel-Finance/scrivel/tree/main/scrivel/examples)
dedicated to just this. Scrivel shows everything from basic reads to more involved writes to entire market-making
operations. 

Remember that Swivel.py is a library with a very specific, and narrow, use case. Present the
Swivel protocol as an object oriented, pythonic collection ready to be used in your own scripting.

---------------------------

### Vendors
One principal concept to grasp is that Swivel.py relies on what in refers to as a `vendor` to handle low-level
chores related to the Ethereum network. Web3.py is a supported vendor at this time, and there may be more in
the future.

#### W3
The W3 Vendor class is a Web3.py specific Vendor that can be used with the Swivel.py Higher Order Contracts.
Constructed with a Web3.py specific `Provider`, our class exposes (hoists) some useful methods from within
Web3 itself.

You can see the Vendor class in use throught the [Scrivel examples](https://github.com/Swivel-Finance/scrivel/tree/main/scrivel/examples)

##### Signer
Our W3 class also constructs and appends a Signer class to itself. This is an abstraction of the 
EIP712 logic needed to sign a Swivel Order _offline_. You generally will not interact with the Signer
directly as the Vendor itself exposes a `sign_order` method. Also note that, in order to sign an order
_offline_ you need to be in possession of the private key associated with the address of the order's 
_maker_. See [here](order_examples) for an example.

##### Private Key
As mentioned above, you must have acess to the private key intented to be used for signing transactions _offline_ and it should be
exported to your shell as `PRIVATE_KEY`, this is used locally and never broadcast or exposed in any way.

---------------------------

### Higher Order Contracts
There are classes present for exposing the A.P.I (ABI) of deployed Swivel smart contracts in a pyhtonic way. Primarily

* swivel.py
* market_place.py

will be your places of contact, as shown in [Scrivel](https://github.com/Swivel-Finance/scrivel/tree/main/scrivel/examples). There is a contract present for the VaultTracker which, 
while typically used internally by the MarketPlace, can be used in isolation to check balances.

The H.O.Cs are constructed with a Vendor instance, then connected to a deployment via the `at` method. Once established,
the contract is ready to be used.

##### Opts
Note that all H.O.C method signatures match the exposed signatures of Swivel smart contract methods. There is also,
in every case, an optional `opts` keyword that may be passed. This argument can be omitted in `call` (read) type
operations generally, but in `send` (write) type operations the user should hydrate important values such as
gas, gasPrice etc...

#### Call, Send (and Transact)
Another principal concept to grasp when using Swivel Higher Order Contracts is that the exposed methods do not
attempt an actual low level `call` or `send` (read and write) type operation. Instead, a tuple of length 2
is always returned from any method invocation. The 2nd item in the tuple is always the `opts` dictionary (or None).
Operations that are `send` (write) type will always assure that the `from` key is set with the users address. Any
other important values (gas, gasPrice, etc...) should be set by the user by using the `opts` dictionary
as described above.

The first item of the tuple will be, depending on the type (call, send), a _callable_ or _transactable_ object.
Callable objects may be wrapped in the `call` helper to execute. Public constants and variables as well as any
non-state-changing getters fall under this category. [Swivel calls](https://github.com/Swivel-Finance/scrivel/blob/main/scrivel/examples/swivel_calls.py) for example. Transactable objects
are, intentionally, handled differently and are the reason why Swivel.py returns a tuple from contract method invocations.
State changing send type operations require a signature, unless the account being used in unlocked. You are likely
not working with unlocked accounts (except perhaps if you are hosting your own node and have your account unlocked locally, see below).
Swivel.py exposes methods on the Vendor class (build_transaction, sign_transaction, etc...) to facilitate signing
_offline_ (given you have exported the correct private key to your shell). The convenience method `send` builds, signs
and broadcasts an offline transaction. See [here](https://github.com/Swivel-Finance/scrivel/blob/main/scrivel/examples/order_examples.py) for
some examples.

In the case you are working with unlocked accounts you can use the `transact` helper directly as there is no need to sign
