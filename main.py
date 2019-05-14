import spotframework.net.user as userclass
import spotframework.net.network as networkclass
import spotframework.net.network as playlist

if __name__ == '__main__':
    print('hello world')

    network = networkclass.network(userclass.User())

    # network.setVolume(105)

    network.getPlaylist('000Eh2vXzYGgrEFlgcWZj3')

    playlist = network.makePlaylist('new playlist')

    network.addPlaylistTracks(playlist.playlistid, ["spotify:track:78lC4VmDVSSsCUQ0VNdQva"]*149)

    network.replacePlaylistTracks(playlist.playlistid, ["spotify:track:78lC4VmDVSSsCUQ0VNdQva"] * 160)

    network.pause()

    #network.getPlayer()

    # playlists = network.getUserPlaylists()
    # for playlist in playlists:
    #     print(playlist.name + ' ' + playlist.playlistid)