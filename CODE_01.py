# Import relevant namespace:
import NXOpen
import NXOpen.Features
import NXOpen.Facet
import NXOpen.MenuBar

import json


def main():
    # setting data values
    data_list = []
    value1 = 0

    stature_list = [1500.0, 1600.0, 1700.0, 1800.0, 1900.0]
    weight_list = [50.0, 60.0, 75.0, 85.0, 95.0]
    waist_list = [650.0, 750.0, 850.0, 1000.0, 1150.0]
    hatch_list = [1, 2, 3, 4, 5, 6, 7]
    skeg_list = [True, False]
    rudder_list = [True, False]

    theSession = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display

# -------------------------------------------------------------------------------------------------------------------- #
    def hatch_bulkhead(hatch):
        markId7 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Edit Hatch + Bulkhead")

        # Bulk head associated with day hatch:
        features1 = [NXOpen.Features.Feature.Null] * 1
        extrude1 = workPart.Features.FindObject("EXTRUDE(44)")
        features1[0] = extrude1

        # LHS day hatch
        features2 = [NXOpen.Features.Feature.Null] * 1
        featureGroup1 = workPart.Features.FindObject("FEATURE_SET(66)")
        features2[0] = featureGroup1

        # RHS day hatch
        features3 = [NXOpen.Features.Feature.Null] * 1
        featureGroup2 = workPart.Features.FindObject("FEATURE_SET(57)")
        features3[0] = featureGroup2

        # Rear Storage
        features4 = [NXOpen.Features.Feature.Null] * 1
        featureGroup3 = workPart.Features.FindObject("FEATURE_SET(75)")
        features4[0] = featureGroup3

        # Front Storage
        features5 = [NXOpen.Features.Feature.Null] * 1
        featureGroup4 = workPart.Features.FindObject("FEATURE_SET(84)")
        features5[0] = featureGroup4

        if hatch == 1:  # 1 = day hatch LHS
            workPart.Features.SuppressFeatures(features3)
            workPart.Features.SuppressFeatures(features4)
            workPart.Features.SuppressFeatures(features5)
            errorFeatures1 = workPart.Features.UnsuppressFeatures(features1)
            errorFeatures2 = workPart.Features.UnsuppressFeatures(features2)

        elif hatch == 2:  # 2 = day hatch RHS
            workPart.Features.SuppressFeatures(features2)
            workPart.Features.SuppressFeatures(features4)
            workPart.Features.SuppressFeatures(features5)
            errorFeatures1 = workPart.Features.UnsuppressFeatures(features1)
            errorFeatures3 = workPart.Features.UnsuppressFeatures(features3)

        elif hatch == 3:  # 3 = day hatch LHS + Rear Storage
            workPart.Features.SuppressFeatures(features3)
            workPart.Features.SuppressFeatures(features5)
            errorFeatures1 = workPart.Features.UnsuppressFeatures(features1)
            errorFeatures2 = workPart.Features.UnsuppressFeatures(features2)
            errorFeatures4 = workPart.Features.UnsuppressFeatures(features4)

        elif hatch == 4:  # 4 = day hatch RHS + Rear Storage
            workPart.Features.SuppressFeatures(features2)
            workPart.Features.SuppressFeatures(features5)
            errorFeatures1 = workPart.Features.UnsuppressFeatures(features1)
            errorFeatures3 = workPart.Features.UnsuppressFeatures(features3)
            errorFeatures4 = workPart.Features.UnsuppressFeatures(features4)

        elif hatch == 5:  # 5 = day hatch LHS + Rear Storage + Front Storage
            workPart.Features.SuppressFeatures(features3)
            errorFeatures1 = workPart.Features.UnsuppressFeatures(features1)
            errorFeatures2 = workPart.Features.UnsuppressFeatures(features2)
            errorFeatures4 = workPart.Features.UnsuppressFeatures(features4)
            errorFeatures6 = workPart.Features.UnsuppressFeatures(features5)

        elif hatch == 6:  # 6 = day hatch RHS + Rear Storage + Front Storage
            workPart.Features.SuppressFeatures(features2)
            errorFeatures1 = workPart.Features.UnsuppressFeatures(features1)
            errorFeatures3 = workPart.Features.UnsuppressFeatures(features3)
            errorFeatures4 = workPart.Features.UnsuppressFeatures(features4)
            errorFeatures6 = workPart.Features.UnsuppressFeatures(features5)

        else:  # No day hatch + No storage
            workPart.Features.SuppressFeatures(features1)
            workPart.Features.SuppressFeatures(features2)
            workPart.Features.SuppressFeatures(features3)
            workPart.Features.SuppressFeatures(features4)
            workPart.Features.SuppressFeatures(features5)

        nErrs7 = theSession.UpdateManager.DoUpdate(markId7)

    def additional_feature(skeg, rudder):
        markId8 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Edit Additional Features")

        # skeg
        features6 = [NXOpen.Features.Feature.Null] * 1
        featureGroup5 = workPart.Features.FindObject("FEATURE_SET(94)")
        features6[0] = featureGroup5

        # rudder
        features7 = [NXOpen.Features.Feature.Null] * 1
        featureGroup6 = workPart.Features.FindObject("FEATURE_SET(117)")
        features7[0] = featureGroup6

        if skeg:
            errorFeatures7 = workPart.Features.UnsuppressFeatures(features6)
        else:
            workPart.Features.SuppressFeatures(features6)

        if rudder:
            errorFeatures8 = workPart.Features.UnsuppressFeatures(features7)
        else:
            workPart.Features.SuppressFeatures(features7)

        nErrs8 = theSession.UpdateManager.DoUpdate(markId8)

    # Exports data to file in .STL (provides a log of change also):
    def save_stl(value1):

        markId10 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "STL Export")

        # STL set up:
        sTLCreator1 = theSession.DexManager.CreateStlCreator()
        sTLCreator1.AutoNormalGen = True
        sTLCreator1.ChordalTol = 0.080000000000000002
        sTLCreator1.AdjacencyTol = 0.080000000000000002

        # Output path:
        sTLCreator1.OutputFile = f"D:\\path\\Kayak_{str(value1)}.stl"

        # Adding Bodies to STL export:
        objects1 = [NXOpen.NXObject.Null] * 13
        body1 = workPart.Bodies.FindObject("EXTRUDE(78)")
        objects1[0] = body1
        body2 = workPart.Bodies.FindObject("EXTRUDE(46)")
        objects1[1] = body2
        body3 = workPart.Bodies.FindObject("EXTRUDE(71)")
        objects1[2] = body3
        body4 = workPart.Bodies.FindObject("EXTRUDE(106)")
        objects1[3] = body4
        body5 = workPart.Bodies.FindObject("EXTRUDE(54)")
        objects1[4] = body5
        body6 = workPart.Bodies.FindObject("EXTRUDE(44)")
        objects1[5] = body6
        body7 = workPart.Bodies.FindObject("EXTRUDE(52)")
        objects1[6] = body7
        body8 = workPart.Bodies.FindObject("EXTRUDE(100)")
        objects1[7] = body8
        body9 = workPart.Bodies.FindObject("EXTRUDE(60)")
        objects1[8] = body9
        body10 = workPart.Bodies.FindObject("EXTRUDE(92)")
        objects1[9] = body10
        body11 = workPart.Bodies.FindObject("EXTRUDE(62)")
        objects1[10] = body11
        body12 = workPart.Bodies.FindObject("EXTRUDE(43)")
        objects1[11] = body12
        body13 = workPart.Bodies.FindObject("EXTRUDE(45)")
        objects1[12] = body13
        added1 = sTLCreator1.ExportSelectionBlock.Add(objects1)

        nXObject1 = sTLCreator1.Commit()
        sTLCreator1.Destroy()

        nErrs10 = theSession.UpdateManager.DoUpdate(markId10)

# -------------------------------------------------------------------------------------------------------------------- #
# OUTPUT STAGE

    for weight in weight_list:
        for waist in waist_list:
            for skeg in skeg_list:
                for rudder in rudder_list:
                    for hatch in hatch_list:

                        # Marks point for rollback if errors encountered
                        markId1 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible,
                                                         "Set Width + Length")

                        if weight < 55.0:
                            kayak_width = 480.0
                            kayak_length = 4500.0

                        elif 55.0 <= weight <= 70.0:
                            kayak_width = 500.0
                            kayak_length = 4500.0

                        elif 71.0 <= weight <= 80.0:
                            kayak_width = 500.0
                            kayak_length = 5000.0

                        elif 81.0 <= weight <= 90.0:
                            kayak_width = 550.0
                            kayak_length = 5000.0

                        elif weight > 90.0:
                            kayak_width = 600.0
                            kayak_length = 5500.0
                        else:
                            kayak_length = 5500.0
                            kayak_width = 600.0

                        nErrs1 = theSession.UpdateManager.DoUpdate(markId1)

                        markId2 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Set Cockpit Width")

                        if waist < 700.0 and kayak_width >= 480.0:
                            cockpit_width = 400.0

                        elif 701.0 <= waist <= 800.0 and kayak_width >= 500.0:
                            cockpit_width = 430.0

                        elif 801.0 <= waist <= 950.0 and kayak_width >= 550.0:
                            cockpit_width = 450.0

                        elif 951.0 <= waist <= 1100.0 and kayak_width >= 550.0:
                            cockpit_width = 470.0

                        elif waist > 1100.0 and kayak_width >= 600.0:
                            cockpit_width = 490.0

                        elif waist > 1100.0 and kayak_width < 600.0:
                            cockpit_width = 430.0
                        else:
                            cockpit_width = 400.0

                        nErrs2 = theSession.UpdateManager.DoUpdate(markId2)

                        # Runs functions:
                        theSession.Preferences.Modeling.UpdatePending = False

                        markId3 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Edit Dimensions")

                        # Length
                        expression1 = workPart.Expressions.FindObject("kayak_length")
                        unit1 = workPart.UnitCollection.FindObject("MilliMeter")
                        workPart.Expressions.EditWithUnits(expression1, unit1, str(kayak_length))

                        # Width
                        expression2 = workPart.Expressions.FindObject("kayak_width")
                        unit1 = workPart.UnitCollection.FindObject("MilliMeter")
                        workPart.Expressions.EditWithUnits(expression2, unit1, str(kayak_width / 2))

                        nErrs3 = theSession.UpdateManager.DoUpdate(markId3)

                        markId4 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Edit Cockpit")

                        # Cockpit Width
                        expression3 = workPart.Expressions.FindObject("cockpit_width")
                        unit2 = workPart.UnitCollection.FindObject("MilliMeter")
                        workPart.Expressions.EditWithUnits(expression3, unit2, str(cockpit_width))

                        nErrs4 = theSession.UpdateManager.DoUpdate(markId4)

                        markId5 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Set Hatch Config")

                        if hatch == 1:  # 1 = day hatch LHS
                            hatch_config = "Day Hatch on left side"

                        elif hatch == 2:  # 2 = day hatch RHS
                            hatch_config = "Day Hatch on right side"

                        elif hatch == 3:  # 3 = day hatch LHS + Rear Storage
                            hatch_config = "Day Hatch on left side + Rear storage"

                        elif hatch == 4:  # 4 = day hatch RHS + Rear Storage
                            hatch_config = "Day Hatch on right side + Rear storage"

                        elif hatch == 5:  # 5 = day hatch LHS + Rear Storage + Front Storage
                            hatch_config = "Day Hatch on right side + Rear storage + Front storage"

                        elif hatch == 6:  # 6 = day hatch RHS + Rear Storage + Front Storage
                            hatch_config = "Day Hatch on right side + Rear storage + Front storage"

                        else:  # No day hatch + No storage
                            hatch_config = "No storage"

                        nErrs5 = theSession.UpdateManager.DoUpdate(markId5)

                        markId6 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Set Additional Config")

                        if skeg:
                            skeg_config = "Yes"
                        else:
                            skeg_config = "No"

                        if rudder:
                            rudder_config = "Yes"
                        else:
                            rudder_config = "No"

                        nErrs6 = theSession.UpdateManager.DoUpdate(markId6)

                        hatch_bulkhead(hatch)
                        additional_feature(skeg, rudder)

                        markId9 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible,
                                                         "Set Volume")

                        measureBodyBuilder1 = workPart.MeasureManager.CreateMeasureBodyBuilder(
                            NXOpen.NXObject.Null)

                        bodies1 = [NXOpen.Body.Null] * 13
                        body1 = workPart.Bodies.FindObject("EXTRUDE(78)")
                        bodies1[0] = body1
                        body2 = workPart.Bodies.FindObject("EXTRUDE(52)")
                        bodies1[1] = body2
                        body3 = workPart.Bodies.FindObject("EXTRUDE(44)")
                        bodies1[2] = body3
                        body4 = workPart.Bodies.FindObject("EXTRUDE(106)")
                        bodies1[3] = body4
                        body5 = workPart.Bodies.FindObject("EXTRUDE(71)")
                        bodies1[4] = body5
                        body6 = workPart.Bodies.FindObject("EXTRUDE(43)")
                        bodies1[5] = body6
                        body7 = workPart.Bodies.FindObject("EXTRUDE(60)")
                        bodies1[6] = body7
                        body8 = workPart.Bodies.FindObject("EXTRUDE(45)")
                        bodies1[7] = body8
                        body9 = workPart.Bodies.FindObject("EXTRUDE(54)")
                        bodies1[8] = body9
                        body10 = workPart.Bodies.FindObject("EXTRUDE(62)")
                        bodies1[9] = body10
                        body11 = workPart.Bodies.FindObject("EXTRUDE(92)")
                        bodies1[10] = body11
                        body12 = workPart.Bodies.FindObject("EXTRUDE(100)")
                        bodies1[11] = body12
                        body13 = workPart.Bodies.FindObject("EXTRUDE(46)")
                        bodies1[12] = body13
                        bodyDumbRule1 = workPart.ScRuleFactory.CreateRuleBodyDumb(bodies1, True)

                        rules1 = [None] * 1
                        rules1[0] = bodyDumbRule1
                        measureBodyBuilder1.BodyCollector.ReplaceRules(rules1, False)

                        massUnits1 = [NXOpen.Unit.Null] * 5
                        unit1 = workPart.UnitCollection.FindObject("SquareMilliMeter")
                        massUnits1[0] = unit1
                        unit2 = workPart.UnitCollection.FindObject("CubicMilliMeter")
                        massUnits1[1] = unit2
                        unit3 = workPart.UnitCollection.FindObject("Kilogram")
                        massUnits1[2] = unit3
                        unit4 = workPart.UnitCollection.FindObject("MilliMeter")
                        massUnits1[3] = unit4
                        unit5 = workPart.UnitCollection.FindObject("Newton")
                        massUnits1[4] = unit5

                        measureBodies1 = workPart.MeasureManager.NewMassProperties(massUnits1,
                                                                                   0.98999999999999999, False,
                                                                                   measureBodyBuilder1.BodyCollector)

                        volume = measureBodies1.Volume / 1000000000

                        nErrs9 = theSession.UpdateManager.DoUpdate(markId9)

                        for stature in stature_list:
                            data = {
                                "variant": value1,          # Float
                                "stature": stature,         # Float
                                "weight": weight,           # Float
                                "length": kayak_length,     # Float
                                "width": kayak_width,       # Float
                                "waist": waist,             # Float
                                "skeg": skeg_config,        # String
                                "rudder": rudder_config,    # String
                                "hatch": hatch_config,      # String
                                "volume": volume,           # Float
                                "cad": f"https://firebasestorage.googleapis.com/v0/b/bucketname.appspot.com/o/kayak_{value1}.stl?alt=media"
                                }

                            data_list.append(data)

                            # Triggers file export
                            save_stl(value1)
                            value1 += 1

                            markId11 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Export JSON")

                            write_path = 'C:path/data.json'

                            with open(write_path, 'w', encoding='utf-8') as f:
                                json.dump(data_list, f, ensure_ascii=False, indent=4)

                            nErrs11 = theSession.UpdateManager.DoUpdate(markId11)

# -------------------------------------------------------------------------------------------------------------------- #

# Run condition:


if __name__ == '__main__':
    main()
