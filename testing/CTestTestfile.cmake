
set(TEST_LIST
    TestImages_RequiredFields
    TestImages_SuperfluousFields
    TestImages_StringFieldsFormat
    TestImages_UniqueName
#    TestImages_CoordFieldsFormat
#    TestImages_StartupView

    TestSessions_RequiredFields
    TestSessions_SuperfluousFields
    TestSessions_StringFieldsFormat
    TestSessions_UniqueName
    TestSessions_ImagesList

    TestImageData_RequiredFields
    TestImageData_SuperfluousFields
    TestImageImageData_Correspondence
   )

foreach(TEST_NAME ${TEST_LIST})
    ADD_TEST( ${TEST_NAME} "test_database.py" ${TEST_NAME} $ENV{DB_HOST} $ENV{DB_NAME} )
endforeach(TEST_NAME)

