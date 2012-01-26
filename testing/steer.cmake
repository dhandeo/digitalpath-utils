set(CTEST_SITE slide-atlas)


set(DB_INSTANCES
    "slide-atlas.org bev1"
    "slide-atlas.org paul3"
    "slide-atlas.org demo"
    "ayodhya bev1"
    "ayodhya paul2"
    "ayodhya paul2copy"
    "ayodhya demo"
   )




set(MODEL Nightly)
set(CTEST_TIMEOUT "7200")

set(CTEST_DASHBOARD_ROOT    "$ENV{HOME}/Desktop/digitalpath/digitalpath-utils/testing")
set(CTEST_SOURCE_DIRECTORY  "${CTEST_DASHBOARD_ROOT}")
set(CTEST_BINARY_DIRECTORY  "${CTEST_SOURCE_DIRECTORY}")

set(CTEST_BUILD_COMMAND "true")

foreach(DB_INSTANCE ${DB_INSTANCES})
    separate_arguments(DB_INSTANCE_ WINDOWS_COMMAND ${DB_INSTANCE})
    list(GET DB_INSTANCE_ 0 DB_HOST)
    set(ENV{DB_HOST} ${DB_HOST})
    list(GET DB_INSTANCE_ 1 DB_NAME)
    set(ENV{DB_NAME} ${DB_NAME})

    set(CTEST_BUILD_NAME "$ENV{DB_HOST} : $ENV{DB_NAME}")

    ctest_start(${MODEL} TRACK ${MODEL})
    ctest_build() # triggers overwrite of previous results
    ctest_test(BUILD  "${CTEST_BINARY_DIRECTORY}")
    ctest_submit(PARTS Test)

endforeach(DB_INSTANCE)

