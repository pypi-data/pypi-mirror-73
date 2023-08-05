# lib_hal9k

The **HackerLab 9000** controller library.

(Note: This project is unaffiliated with the [Android Mod](http://hal9k.ru/) which goes by the name `Hal9k`.)

## Lingo

This library is designed to provide the simplest possible API for controlling
VirtualBox VMs, without any of the fancy stuff. There are only three actions
we care about:

* Starting the VM.
* Stopping the VM.
* Reverting the VM to the most recent snapshot.

This functionality is similar to that of a basic music player, which provides a familiar metaphor. In the language of this library, a VM is a "Track," which you can "play," "rewind," or "stop."

The Meta controller can list and retrieve tracks.

## Demo

```python
>>> from hal9k import Meta
>>> # Instantiate a Meta controller.
>>> meta = Meta()
>>> # Retrieve a track listing.
>>> meta.get_tracks()
['Debian 9.12 x64 (BASE)', 'Windows 8 x64 (BASE)', 'MSEdge - Win10 (BASE)', 'Debian 10.3 x64 (BASE)']
>>> # Instantiate a Track controller.
>>> track = meta.fetch('Debian 9.12 x64 (BASE)')
>>> # Start the track.
>>> track.play()
>>> # Check that it's running.
>>> track.status()
1
>>> # Stop the track.
>>> track.stop()
>>> # Check that it's stopped.
>>> track.status()
0
>>> # Rewind the track.
>>> track.rewind()
```

## How it Works

The `Meta.get_tracks` function returns a list of the names of all VMs which have a `PRODUCTION` snapshot defined. The `Track.rewind` function restores the track's `PRODUCTION` snapshot. There can be only one `PRODUCTION` shapshot for each VM. If you decide to make a new `PRODUCTION` snapshot, be sure to delete the one previous. Any VMs lacking a `PRODUCTION` snapshot will be invisible to `hal9k`.

An exception will be raised for `Track.play` and `Track.rewind` if the track is already playing. Likewise for `Track.stop` if the track is already stopped. Tracks must be stopped before using `Track.play` or `Track.rewind`, and tracks must be playing before using `Track.stop`.

## Changelog

* **0.6.1** :: Updated `Meta.get_tracks` function to list only production-ready VMs.
* **0.6.0** :: Added `rewind` function to `Track` class.
* **0.5.0** :: Added `status` function to `Track` class.
* **0.4.0** :: Added `stop` function to `Track` class.
* **0.3.0** :: Added `Track` class with `play` function.
* **0.2.0** :: Added `fetch` function to `Meta` class.
* **0.1.0** :: Added `Meta` class with `get_tracks` function.
