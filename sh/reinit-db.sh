#!/bin/bash

dropdb -U sample $1;
createdb -U sample $1;