import time
from django.http import HttpResponse, JsonResponse
from ..sdks.Tobii.eye_tracker import TobiiController


from ..lib.emdat.utils import cast_int, cast_float
from ..lib.emdat.Recording import read_aoilines, get_pupil_size, get_distance
from ..lib.emdat.data_structures import Datapoint, Fixation
from ..lib.emdat.Segment import Segment
from ..lib.emdat.AOI import AOI
from itertools import izip


trackers = {}


def list(request):

    type = request.GET.get('type')

    if (type == 'tobiiv3'):
        eb = TobiiController()

        time.sleep(10)

        if eb.eyetrackers:
            print eb.eyetrackers

        eb.destroy()

    return JsonResponse({'trackers':'TT120-204-80900268'}, status=200)


def connect(request):

    type = request.GET.get('type')

    if (type == 'tobiiv3'):

        tobii = TobiiController()
        time.sleep(5)
        tobii.activate('TT120-204-80900268')
        trackers['TT120-204-80900268'] = {'object':tobii, 'type':'tobiiv3'}

    return JsonResponse({'status':'done'}, status=200)



def disconnect(request, id):

    a =  trackers

    tracker = trackers[str(id)]

    tracker['object'].destroy()

    return JsonResponse({'status':'done'}, status=200)



def start_tracking(request, id):

    tracker = trackers[str(id)]
    tracker['object'].startTracking()

    return JsonResponse({'status':'done'}, status=200)


def get_features(request, id):

    features = {}

    if str(id) in trackers:
        tracker = trackers[str(id)]
        gaze_data = tracker['object'].gazeData

        data = []

        for gaze in gaze_data:

            if gaze.LeftValidity < 2 or gaze.RightValidity < 2:
                pupil_left = cast_float(gaze.LeftPupil, -1)
                pupil_right = cast_float(gaze.RightPupil, -1)
                distance_left = cast_float(gaze.RightEyePosition3D.z, -1)
                distance_right = cast_float(gaze.LeftEyePosition3D.z, -1)
                data.append({"timestamp": gaze.Timestamp,
                    "pupilsize": get_pupil_size(pupil_left, pupil_right),
                    "distance": get_distance(distance_left, distance_right),
                    "is_valid": True,
                    "stimuliname": 'T',
                    "fixationindex": 0,
                    "gazepointxleft": gaze.LeftGazePoint2D})



        #print data


        gaze_points = map(Datapoint, data)
        fixations = []

        aoi = []
        aoi.append(AOI('right', [(641,0), (1280,0), (1280,1024), (641, 1024)], [], [])) #641,0\t1280,0\t1280,1024\t641,1024

        # Create segment object
        segment = Segment('0', gaze_points, fixations, aois=aoi, rest_pupil_size=1)

        # Get features
        feature_names, feature_values = segment.get_features()

        # Convert to a dictionary
        features = dict(izip(feature_names, feature_values))

        tracker['object'].gazeData = []

    return JsonResponse(features, status=200)


def stop_tracking(request, id):

    tracker = trackers[str(id)]
    tracker['object'].stopTracking()

    tracker['object'].destroy()

    return JsonResponse({'status':'done'}, status=200)