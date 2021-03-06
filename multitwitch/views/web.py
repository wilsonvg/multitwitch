import configparser
import requests
import json

from multitwitch.lib.session import web, ajax
from pyramid.response import FileResponse

import multitwitch.lib.twitch as T
import multitwitch.lib.streamlister as sl

class WebView:

    @web(template="web/home.tmpl")
    def home(request):
        config = configparser.ConfigParser()
        config.read('config.ini')
        default = config['DEFAULT']
        community_name = default.get('community_name', 'x3lgaming')
        title = default.get('title', 'X3LGaming Multitwitch')
        base_url = default.get('base_url', 'http://rtmp.roaet.com:5000')

        streamlister = sl.StreamLister(config)
        community_streams = streamlister.get_community_streams_by_name(
            community_name)
        staff_picks = streamlister.get_staff_picks()
        return {'project' : title,
                'streams' : [],
                'community_streams': community_streams,
                'community_name': community_name,
                'staff_picks': staff_picks,
                'base_url' : base_url,
                'unique_streams' : [],
                'nstreams' : len([])}

    @web(template="web/home.tmpl")
    def edit(request):
        config = configparser.ConfigParser()
        config.read('config.ini')
        default = config['DEFAULT']
        community_name = default.get('community_name', 'x3lgaming')
        title = default.get('title', 'X3LGaming Multitwitch')
        base_url = default.get('base_url', 'http://rtmp.roaet.com:5000')

        streamlister = sl.StreamLister(config)
        community_streams = streamlister.get_community_streams_by_name(
            community_name)
        staff_picks = streamlister.get_staff_picks()

        path = request.path
        print path
        if path.startswith('/'): # removes front slash /edit/ -> edit/
            path = path[1:]
        if path.endswith('/'): # removes back flash
            path = path[:-1]
        path_parts = path.split("/")
        if len(path_parts) <= 1: # if only edit
            return "REDIRECT:root:"
        stream_list = path_parts
        stream_list.pop(0) # removes 'edit'
        edit_string = '/'.join(stream_list)
        print stream_list
        return {'project' : title,
                'streams' : stream_list,
                'community_streams': community_streams,
                'community_name': community_name,
                'staff_picks': staff_picks,
                'base_url' : base_url,
                'unique_streams' : [],
                'edit_string': edit_string,
                'nstreams' : len(stream_list)}

    @web()
    def view(request):
        stream_list = []
        layout = 'layout0'
        if len(request.GET) == 0:
            return "REDIRECT:root:"
        for idx in xrange(7):
            key = 's%d' % idx
            if len(request.GET[key]) > 0:
                stream_list.append(request.GET[key])
        if len(request.GET['layout']) > 0:
            layout = "layout%s" % request.GET['layout']
        stream_list.append(layout)
        path = '/'.join(stream_list)
        return "REDIRECT:multitwitch:%s" % path

    @web(template="web/streams.tmpl")
    def streams(request):
        config = configparser.ConfigParser()
        config.read('config.ini')
        default = config['DEFAULT']
        community_name = default.get('community_name', 'x3lgaming')
        title = default.get('title', 'X3LGaming Multitwitch')
        base_url = default.get('base_url', 'http://rtmp.roaet.com:5000')

        path = request.path
        if path.startswith('/'):
            path = path[1:]
        if path.endswith('/'):
            path = path[:-1]
        path_parts = path.split("/")
        if len(path_parts) <= 1:
            return "REDIRECT:root:"
        if 'layout' not in path_parts[-1]:
            path = '/'.join(path_parts)
            path = '%s/layout0' % path
            return "REDIRECT:multitwitch:%s" % path
        stream_list = path_parts[:-1]
        edit_string = '/'.join(stream_list)
        return {'project' : title,
                'streams' : stream_list,
                'base_url' : base_url,
                'unique_streams' : [],
                'edit_string': edit_string,
                'nstreams' : len(stream_list)}

    @web()
    def twitch_api_test(request):
        config = configparser.ConfigParser()
        default = config['DEFAULT']
        community_name = default.get('community_name', 'x3lgaming')
        title = default.get('title', 'X3LGaming Multitwitch')
        base_url = default.get('base_url', 'http://rtmp.roaet.com:5000')

        streamlister = sl.StreamLister(config)
        stream_list = streamlister.get_community_streams_by_name(
            community_name)
        return str(stream_list)

    @staticmethod
    def favicon(request):
        return FileResponse("multitwitch/static/favicon.ico", content_type="image/x-icon")
