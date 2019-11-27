# Created by K McMaster on the 14/11/2019
# Journal created for use with SIEMENS NX 12.0 software
# For use with CAD file:
# Coded as part of the 2019 Chalmers University of Technology DiLAM project using Python 3.7
# Working in coordination with the University of Strathclyde Mechanical and Aerospace department
# Refer to handover document for further information
# Last Edited 25/11/2019

# Import relevant namespace:
import NXOpen
import NXOpen.Features
import NXOpen.Facet
import NXOpen.MenuBar

import json


def main():

    # setting data values
    value1 = 0
    stature_list = [1625.0, 1778.0, 1828.0, 1930.0]  # 5'4", 5'10", 6'0", 6'4" (in mm)
    weight_list = [50.0, 70.0, 80.0, 95.0]  # kg
    waist_list = [650.0, 760.0, 840.0, 1000.0, 1150.0]  # mm
    hatch_list = [1, 2, 3, 4, 5, 6, 7]
    skeg_list = [True, False]
    rudder_list = [True, False]
    thigh_brace_list = [True, False]
    volume_list = [0, 1]
    hatch_config = ""
    length = 0
    width = 0

    theSession = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display

# -------------------------------------------------------------------------------------------------------------------- #

    def dimension_change(stature, weight, length, width):

        theSession.Preferences.Modeling.UpdatePending = False

        # Marks point for rollback if errors encountered
        markId1 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Edit Human")

        humanBuilder1 = workPart.Features.CreateHumanBuilder(NXOpen.Features.Feature.Null)

        # Used to define human stature and weight:

        humanBuilder1.SetStatureData(NXOpen.HumanData.StatureType.Custom, 1750.0, NXOpen.HumanData.StatureUnitType.Mm)
        humanBuilder1.SetWeightData(NXOpen.HumanData.WeightType.Custom, 78.0, NXOpen.HumanData.WeightUnitType.Kg)
        humanBuilder1.SetExpressionStatureData(str(stature))
        humanBuilder1.SetExpressionWeightData(str(weight))

        feature1 = humanBuilder1.CommitFeature()
        humanBuilder1.Destroy()

        theSession.Preferences.Modeling.UpdatePending = False
        theSession.Preferences.Modeling.UpdatePending = False
        theSession.CleanUpFacetedFacesAndEdges()

        nErrs1 = theSession.UpdateManager.DoUpdate(markId1)

        if stature < 1550 or weight < 55:  # XS
            width = 450
            length = 4500

        if stature == range(1550, 1650) or weight == range(55, 70):  # S
            width = 500
            length = 4500

        elif stature == range(1651, 1750) or weight == range(71, 80):  # M
            width = 500
            length = 5000

        elif stature == range(1751, 1850) or weight == range(81, 90):  # L
            width = 550
            length = 5000

        elif stature > 1850.0 or weight > 90.0:  # XL
            width = 600
            length = 5500

        markId2 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Edit Dimensions")

        # Finds object, unit and then applies a value:
        # Width
        expression1 = workPart.Expressions.FindObject("width")
        unit1 = workPart.UnitCollection.FindObject("MilliMeter")
        workPart.Expressions.EditWithUnits(expression1, unit1, str(width/2))

        # Length
        expression2 = workPart.Expressions.FindObject("Length")
        workPart.Expressions.EditWithUnits(expression2, unit1, str(length))

        nErrs2 = theSession.UpdateManager.DoUpdate(markId2)

    def cockpit_change(waist):
        markId3 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Edit Cockpit")

        if waist < 700:  # XS
            cockpit_width = 400

        elif waist == range(701, 800):  # S
            cockpit_width = 450

        elif waist == range(801, 950):  # M
            cockpit_width = 450

        elif waist == range(951, 1100):  # L
            cockpit_width = 500

        elif waist > 1100:
            cockpit_width = 550  # XL

        # Cockpit Width
        expression3 = workPart.Expressions.FindObject("cockpit_width")
        unit1 = workPart.UnitCollection.FindObject("MilliMeter")
        workPart.Expressions.EditWithUnits(expression3, unit1, str(cockpit_width))

        nErrs3 = theSession.UpdateManager.DoUpdate(markId3)

    def hatch_bulkhead(hatch, hatch_config):
        markId4 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Hatch+Bulkhead")

        # Bulk head associated with day hatch:
        features1 = [NXOpen.Features.Feature.Null] * 1
        extrude1 = workPart.Features.FindObject("EXTRUDE(44)")
        features1[0] = extrude1

        # LHS day hatch
        features2 = [NXOpen.Features.Feature.Null] * 1
        featureGroup1 = workPart.Features.FindObject("FEATURE_SET(67)")
        features2[0] = featureGroup1

        # RHS day hatch
        features3 = [NXOpen.Features.Feature.Null] * 1
        featureGroup2 = workPart.Features.FindObject("FEATURE_SET(58)")
        features3[0] = featureGroup2

        # Rear Storage
        features4 = [NXOpen.Features.Feature.Null] * 1
        featureGroup3 = workPart.Features.FindObject("FEATURE_SET(76)")
        features4[0] = featureGroup3

        # Front Storage
        features5 = [NXOpen.Features.Feature.Null] * 1
        featureGroup4 = workPart.Features.FindObject("FEATURE_SET(85)")
        features5[0] = featureGroup4

        if hatch == 1:  # 1 = day hatch LHS
            workPart.Features.SuppressFeatures(features3)
            workPart.Features.SuppressFeatures(features4)
            workPart.Features.SuppressFeatures(features5)
            errorFeatures1 = workPart.Features.UnsuppressFeatures(features1)
            errorFeatures2 = workPart.Features.UnsuppressFeatures(features2)

            hatch_config = "Day Hatch on left side"

        elif hatch == 2:  # 2 = day hatch RHS
            workPart.Features.SuppressFeatures(features2)
            workPart.Features.SuppressFeatures(features4)
            workPart.Features.SuppressFeatures(features5)
            errorFeatures1 = workPart.Features.UnsuppressFeatures(features1)
            errorFeatures3 = workPart.Features.UnsuppressFeatures(features3)

            hatch_config = "Day Hatch on right side"

        elif hatch == 3:  # 3 = day hatch LHS + Rear Storage
            workPart.Features.SuppressFeatures(features3)
            workPart.Features.SuppressFeatures(features5)
            errorFeatures1 = workPart.Features.UnsuppressFeatures(features1)
            errorFeatures2 = workPart.Features.UnsuppressFeatures(features2)
            errorFeatures4 = workPart.Features.UnsuppressFeatures(features4)

            hatch_config = "Day Hatch on left side + Rear storage"

        elif hatch == 4:  # 4 = day hatch RHS + Rear Storage
            workPart.Features.SuppressFeatures(features2)
            workPart.Features.SuppressFeatures(features5)
            errorFeatures1 = workPart.Features.UnsuppressFeatures(features1)
            errorFeatures3 = workPart.Features.UnsuppressFeatures(features3)
            errorFeatures4 = workPart.Features.UnsuppressFeatures(features4)

            hatch_config = "Day Hatch on right side + Rear storage"

        elif hatch == 5:  # 5 = day hatch LHS + Rear Storage + Front Storage
            workPart.Features.SuppressFeatures(features3)
            errorFeatures1 = workPart.Features.UnsuppressFeatures(features1)
            errorFeatures2 = workPart.Features.UnsuppressFeatures(features2)
            errorFeatures4 = workPart.Features.UnsuppressFeatures(features4)
            errorFeatures6 = workPart.Features.UnsuppressFeatures(features5)

            hatch_config = "Day Hatch on right side + Rear storage + Front storage"

        elif hatch == 6:  # 6 = day hatch RHS + Rear Storage + Front Storage
            workPart.Features.SuppressFeatures(features2)
            errorFeatures1 = workPart.Features.UnsuppressFeatures(features1)
            errorFeatures3 = workPart.Features.UnsuppressFeatures(features3)
            errorFeatures4 = workPart.Features.UnsuppressFeatures(features4)
            errorFeatures6 = workPart.Features.UnsuppressFeatures(features5)

            hatch_config = "Day Hatch on right side + Rear storage + Front storage"

        else:  # No day hatch + No storage
            workPart.Features.SuppressFeatures(features1)
            workPart.Features.SuppressFeatures(features2)
            workPart.Features.SuppressFeatures(features3)
            workPart.Features.SuppressFeatures(features4)
            workPart.Features.SuppressFeatures(features5)

            hatch_config = "No storage"

        nErrs4 = theSession.UpdateManager.DoUpdate(markId4)

    def additional_feature(skeg, rudder, thigh_brace):
        markId5 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Additional Features")

        # skeg
        features6 = [NXOpen.Features.Feature.Null] * 1
        featureGroup5 = workPart.Features.FindObject("FEATURE_SET(95)")
        features6[0] = featureGroup5

        # rudder
        features7 = [NXOpen.Features.Feature.Null] * 1
        featureGroup6 = workPart.Features.FindObject("FEATURE_SET(115)")
        features7[0] = featureGroup6

        # thigh brace
        features8 = [NXOpen.Features.Feature.Null] * 1
        featureGroup7 = workPart.Features.FindObject("FEATURE_SET(135)")
        features8[0] = featureGroup7

        if skeg:
            errorFeatures7 = workPart.Features.UnsuppressFeatures(features6)
        else:
            workPart.Features.SuppressFeatures(features6)

        if rudder:
            errorFeatures8 = workPart.Features.UnsuppressFeatures(features7)
        else:
            workPart.Features.SuppressFeatures(features7)

        # if thigh_brace:
            # errorFeatures9 = workPart.Features.UnsuppressFeatures(features8)
        # else:
            # workPart.Features.SuppressFeatures(features8)

        nErrs5 = theSession.UpdateManager.DoUpdate(markId5)

# -------------------------------------------------------------------------------------------------------------------- #
# OUTPUT STAGE
    # Exports data to file in .STL (provides a log of change also):
    def save_stl(value1):

        markId6 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "STL Export")

        # STL set up:
        sTLCreator1 = theSession.DexManager.CreateStlCreator()
        sTLCreator1.AutoNormalGen = True
        sTLCreator1.ChordalTol = 0.080000000000000002
        sTLCreator1.AdjacencyTol = 0.080000000000000002

        # Output path:
        sTLCreator1.OutputFile = f"D:\\CAD WORKING DIRECTORY\\BULK_DATA\\\Kayak_{str(value1)}.stl"

        # Adding Bodies to STL export:
        objects1 = [NXOpen.NXObject.Null] * 17

        # Bulk head 1, 2, 3, 4
        body1 = workPart.Bodies.FindObject("EXTRUDE(43)")
        objects1[0] = body1
        if hatch != 7:
            body2 = workPart.Bodies.FindObject("EXTRUDE(44)")
            objects1[1] = body2
        body3 = workPart.Bodies.FindObject("EXTRUDE(45)")
        objects1[2] = body3
        body4 = workPart.Bodies.FindObject("EXTRUDE(46)")
        objects1[3] = body4

        # Thigh braces
         # if thigh_brace:
            # body5 = workPart.Bodies.FindObject("EXTRUDE(131)")
            # objects1[4] = body5
            # body6 = workPart.Bodies.FindObject("Mirror Feature(134:1A:1A)")
            # objects1[5] = body6

        # RHS Hatch
        if hatch == [2, 4, 6]:
            body7 = workPart.Bodies.FindObject("EXTRUDE(55)")
            objects1[6] = body7

        # LHS Hatch
        if hatch == [1, 3, 5]:
            body8 = workPart.Bodies.FindObject("EXTRUDE(61)")
            objects1[7] = body8
            body9 = workPart.Bodies.FindObject("EXTRUDE(63)")
            objects1[8] = body9

        # Front hatch
        if hatch == [5, 6]:
            body10 = workPart.Bodies.FindObject("EXTRUDE(79)")
            objects1[9] = body10

        # Rear Hatch
        if hatch == [3, 4, 5, 6]:
            body11 = workPart.Bodies.FindObject("EXTRUDE(72)")
            objects1[10] = body11

        # Skeg
        if skeg:
            body12 = workPart.Bodies.FindObject("EXTRUDE(93)")
            objects1[11] = body12

        # Rudder
        if rudder:
            body13 = workPart.Bodies.FindObject("EXTRUDE(100)")
            objects1[12] = body13
            body14 = workPart.Bodies.FindObject("EXTRUDE(101)")
            objects1[13] = body14
            body15 = workPart.Bodies.FindObject("EXTRUDE(102)")
            objects1[14] = body15
            body16 = workPart.Bodies.FindObject("EXTRUDE(107)")
            objects1[15] = body16
            body17 = workPart.Bodies.FindObject("EXTRUDE(108)")
            objects1[16] = body17

        added1 = sTLCreator1.ExportSelectionBlock.Add(objects1)

        nXObject1 = sTLCreator1.Commit()
        sTLCreator1.Destroy()

        nErrs6 = theSession.UpdateManager.DoUpdate(markId6)

    data_list = []

    markId7 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Run Operations")

    for stature in stature_list:
        for weight in weight_list:
            for waist in waist_list:
                for volume in volume_list:
                    for skeg in skeg_list:
                        for rudder in rudder_list:
                            for hatch in hatch_list:
                                for thigh_brace in thigh_brace_list:

                                    # Runs functions:
                                    dimension_change(stature, weight, length, width)
                                    cockpit_change(waist)
                                    hatch_bulkhead(hatch, hatch_config)
                                    additional_feature(skeg, rudder, thigh_brace)

                                    data = {
                                        "variant": value1,
                                        "stature": stature,
                                        "weight": weight,
                                        "length": length,
                                        "width": width,
                                        "volume": volume,
                                        "skeg": skeg,
                                        "rudder": rudder,
                                        "hatch": hatch_config,
                                        "thighBraces": thigh_brace
                                    }

                                    data_list.append(data)

                                    # Triggers file export
                                    save_stl(value1)
                                    value1 += 1

    nErrs7 = theSession.UpdateManager.DoUpdate(markId7)

    print(data_list)

    markId8 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Export JSON")

    write_path = 'D:/CAD WORKING DIRECTORY/JSON_DATA/data.json'

    with open(write_path, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)

    nErrs8 = theSession.UpdateManager.DoUpdate(markId8)

# -------------------------------------------------------------------------------------------------------------------- #

# Run condition:


if __name__ == '__main__':
    main()
