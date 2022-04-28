# Algorithm Optimization Challenge

The challenge is to create a program that computes some basic statistics on a collection of small positive integers. You can assume all values will be less than 1,000.

## Requirements

The `DataCapture` object accepts numbers and returns an object for the querying statistics about the inputs. Specifically, the returned object supports querying how many numbers in the collection are less than a value, greater than a value, or within a range.

Here's the program skeleton in python to explain the structure:

```
datacapture = DataCapture()
datacapture.add(3)
datacapture.add(9)
datacapture.add(3)
datacapture.add(4)
datacapture.add(6)
stats = datacapture.build_stats()
stats.less(4) # should return 2 (only two values 3, 3 are less than 4)
stats.between(3, 6) # should return 4 (3, 3, 4 and 6 are between 3 and 6)
stats.greater(4) # should return 2 (6 and  9 are the only two values greater than 4)
```

## Challenge Conditions
 
* You cannot import a library that solves it instantly.
* The methods `add()`, `less()`, `greater()`, and `between()` should have a constant time O(1)
* The method `build_stats()` can be at most linear O(n)
* Apply the best practices you know
* Share a public repo with your project

## Solution

I created an algorithm that implements the following components:

### CapturedNumber

It's a data class that contains all the properties required to pre-computed the statistics of a number:
- `value`: The captured (added) number.
- `count` [default=0]: How many times it has been captured (added).
- `less` [default=0]: how many numbers have a value lower than its value.
- `greater` [default=0]: how many numbers have a value lower than its value.

### CapturedCollection

An iterator that can store `CapturedNumber`s. If a `CapturedCollection` is requested to return a value that is not stored, it will create it on the fly and return it. It makes it possible to iterate over the collection in order, even if the numbers are not added in order.

### DataCapture

A class that allows you to add numbers and pre-compute is statistics. Internally, it uses a `CapturedCollection` and contains the following methods:

#### add

Receive an integer and add it to the `CapturedCollection` as a `CapturedNumber` with `value` equal to the received number, `count` equal to one, `less` equal to zero, and `greater` equal to zero.

If the `CapturedCollection` already contains a `CapturedNumber` with the same value, it simply adds one to the `count` property of the object.

#### build_stats

Iterates over the internal `CapturedCollection` in order, counting the stored `CapturedNumber`s. At the same time, it creates an object of type `Stats` and adds the numbers to that object (not only the stored ones but also the dynamically generated ones). But, before adding it to the `Stats` object, it changes the following properties:

- `less`: based on the previously found `CaptureNumber`s.
- `greater`: based on calculous between the total of `CaptureNumber`s already found during the loop and the total of elements in the collection.

### Stats

A class that uses `CapturedCollection` to do some basic statistics. It assumes that the `CapturedNumber`s in the collections are already pre-computed.

This class contains the following methods:

#### less

Returns the number of `CapturedNumber`s with a value lower than the value of the given number. It takes the value from the `less` attribute of the `CapturedNumber` with the same value of the given number.

#### greater

Returns the number of `CapturedNumber`s with a value higher than the value of the given number. It takes the value from the `greater` attribute of the `CapturedNumber` with the same value of the given number.

#### between

Returns the number of `CapturedNumber`s with a value between two given numbers. It returns the value as the result of calculus between the total of `CapturedNumber`s, `CapturedNumber`s lower than the smallest of the given number, and, `CapturedNumber`s greater than the smallest of the given numbers.

## Setup

> This project uses Python 3.10, other python versions may work, but it is not guaranteed.

- Clone the repo.
- Get into the created folder.
- Create a virtual environment.
- Activate it.
- Install the requirements in the `requirements.txt` file.

## Usage

Run the command: `python src/main.py`

## Testing

Run the command: `mypy . && pytest .`

> Do not forget the dots.
