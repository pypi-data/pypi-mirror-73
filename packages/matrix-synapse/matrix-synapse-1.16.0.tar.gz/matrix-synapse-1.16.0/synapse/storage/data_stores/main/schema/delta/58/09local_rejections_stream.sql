/* Copyright 2020 The Matrix.org Foundation C.I.C
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/*
This migration adds a new `local_rejections_stream` table which records a
stream_ordering for locally-rejected events, so that we can answer the question of
"which rooms had invite rejections between these two stream_orderings?"

the stream_ordering is from the same stream as that of `events`.
*/

CREATE TABLE IF NOT EXISTS local_rejections_stream (
    stream_ordering BIGINT NOT NULL PRIMARY KEY,
    user_id TEXT NOT NULL,
    room_id TEXT NOT NULL,

    FOREIGN KEY (room_id) REFERENCES rooms (room_id)
);

CREATE INDEX IF NOT EXISTS local_rejections_user_stream
   ON local_rejections_stream (user_id, stream_ordering);
